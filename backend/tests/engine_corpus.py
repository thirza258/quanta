"""Record every engine call a test run makes, for replay under the sanitizers.

With QUANTA_ENGINE_CORPUS=path, conftest wraps quanta.engine.call so each
request, the bars it was handed and the response are appended to one binary
file. `make -C backend/engine replay CORPUS=path` replays the file through an
AddressSanitizer/UndefinedBehaviorSanitizer build and requires byte-identical
responses, so the sanitizers see every path the differential tests reach.

Format, little-endian: b"QSCORP01", then records. A market record is b"M",
u32 id, u32 symbols, and per symbol u32 name length, name, i64 bars, u8 price
kind (0 cents int32, 1 float64), u8 volume kind (0 int32, 1 float64), then the
four price rows, volume, time (int64) and day (int32). A call record is b"C",
u32 market id (0xFFFFFFFF for none), u64 + request bytes, u64 + response bytes.
"""

import hashlib
import json
import struct

import numpy as np

NONE = 0xFFFFFFFF


class Recorder:
    def __init__(self, path):
        self.out = open(path, "wb")
        self.out.write(b"QSCORP01")
        self.seen = {}
        self.markets = {}
        self.alive = []
        self.calls = 0

    def close(self):
        self.out.close()

    @staticmethod
    def _body(names, columns):
        parts = [struct.pack("<I", len(columns))]
        for name, column in zip(names, columns, strict=True):
            encoded = name.encode()
            prices = column.cents if column.cents is not None else column.values
            volume = column.volume_int if column.volume_int is not None else column.volume_float
            parts.append(struct.pack("<I", len(encoded)) + encoded)
            parts.append(
                struct.pack(
                    "<qBB",
                    column.length,
                    0 if column.cents is not None else 1,
                    0 if column.volume_int is not None else 1,
                )
            )
            for k in range(4):
                parts.append(np.ascontiguousarray(prices[k]).tobytes())
            parts.append(np.ascontiguousarray(volume).tobytes())
            parts.append(np.ascontiguousarray(column.time, dtype=np.int64).tobytes())
            parts.append(np.ascontiguousarray(column.day, dtype=np.int32).tobytes())
        return b"".join(parts)

    def _market(self, names, columns):
        if not columns:
            return NONE
        # A generated market's arrays are replaced whenever it grows, so their
        # identities name their content; holding them keeps those identities
        # from being reused. Fixtures are small and hashed in full.
        if all(column.cents is not None for column in columns):
            key = tuple((id(c.cents), id(c.volume_int), id(c.time), c.length) for c in columns)
            if key in self.markets:
                return self.markets[key]
            self.alive.append(columns)
        else:
            key = None
        body = self._body(names, columns)
        digest = hashlib.sha1(body).hexdigest()
        if digest not in self.seen:
            self.seen[digest] = len(self.seen)
            self.out.write(b"M" + struct.pack("<I", self.seen[digest]) + body)
        if key:
            self.markets[key] = self.seen[digest]
        return self.seen[digest]

    def wrap(self, run):
        def recorded(payload, columns):
            response = run(payload, columns)
            market = self._market(json.loads(payload)["symbols"], columns)
            self.out.write(b"C" + struct.pack("<IQ", market, len(payload)) + payload)
            self.out.write(struct.pack("<Q", len(response)) + response)
            self.calls += 1
            return response

        return recorded
