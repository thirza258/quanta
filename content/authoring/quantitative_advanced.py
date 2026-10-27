"""Advanced Quantitative Investment Analysis lessons 2.33-2.40, each placed in its book
chapter beside the lesson it builds on. Original lessons with fictional data; each
worksheet runs in the guided runtime and is recomputed independently in
backend/tests/test_advanced_quant_lessons.py."""

from book_courses import q

# (lesson it follows, argument list for the course's add()).
ADVANCED_LESSONS = [
    (
        '2.6',
        (
            '2.33',
            1,
            'Spot rates, forward rates, and discounting with a term structure',
            'Bootstrap spot rates from par yields, derive implied forward rates, and price a coupon bond off the curve instead of with one yield.',
            r"""## The analytical question

Lessons 2.1 and 2.6 discounted every payment with one rate $r$. A single rate is a modelling choice, not a market fact: the market prices a payment due in one year and a payment due in three years at different rates, and the schedule of those rates by maturity is the **term structure**. This lesson swaps the single rate for a curve and works out what changes: what a bond is worth, what the curve implies about future rates, and what a yield to maturity does and does not tell you.

The primitive object is the **discount factor** $d_t$, the price today of a riskless promise of one unit at time $t$. The **spot rate** (zero rate) $s_t$ is the annual rate that links price to payoff, with annual compounding:

$$d_t=\frac{1}{(1+s_t)^{t}}$$

A fixed cash-flow stream is worth each payment times its own discount factor. This is the law of one price: a coupon bond is a bundle of zero-coupon payments, so if its price differs from the bundle's value, buying the cheaper and selling the dearer earns a riskless profit before costs. For annual coupon $C$ and face 100 over $T$ years:

$$P=\sum_{t=1}^{T}C\,d_t+100\,d_T=\sum_{t=1}^{T}\frac{C}{(1+s_t)^{t}}+\frac{100}{(1+s_T)^{T}}$$

**Forward rates.** There are two ways to hold money for $A+B$ years: buy an $(A+B)$-year zero, or buy an $A$-year zero and contract today for the rate on the following $B$ years. No arbitrage forces both routes to the same final amount. The contracted rate is the implied forward rate $f_{A,B}$, the $B$-year rate that starts in $A$ years. Desks write 1y1y for $f_{1,1}$ and 2y1y for $f_{2,1}$.

$$(1+s_{A+B})^{A+B}=(1+s_A)^{A}(1+f_{A,B})^{B}\;\Longrightarrow\;f_{A,B}=\left[\frac{(1+s_{A+B})^{A+B}}{(1+s_A)^{A}}\right]^{1/B}-1=\left[\frac{d_A}{d_{A+B}}\right]^{1/B}-1$$

The one-year case is $f_{1,1}=(1+s_2)^2/(1+s_1)-1$. Chaining forwards rebuilds any spot rate: $(1+s_T)^T$ is the first spot factor times the intervening one-year forward factors, so a spot rate is a geometric average of forwards.

**Bootstrapping.** Markets quote par yields or coupon-bond prices more often than spot rates. The par yield $y_T$ is the coupon rate at which a $T$-year bond is priced at exactly 100:

$$1=y_T\sum_{t=1}^{T}d_t+d_T\;\Longrightarrow\;d_T=\frac{1-y_T\sum_{t=1}^{T-1}d_t}{1+y_T}$$

By the time you reach maturity $T$, every earlier discount factor is known, so each maturity adds exactly one unknown and the curve is solved in order of maturity. That is bootstrapping. A bond quoted at a price $P_T$ away from par, with coupon $C_T$, gives the same step as $d_T=(P_T-C_T\sum_{t<T}d_t)/(100+C_T)$.

**Yield to maturity.** The yield $y$ of a bond is the single rate that solves $P=\sum_t CF_t/(1+y)^t$. It is the IRR of Lesson 2.6 applied to the bond, so it carries the IRR's assumption: the holder earns $y$ a year only if every coupon is reinvested at $y$ until maturity. It summarizes one bond's price; it is not a rate at which new cash flows can be discounted. Two bonds of the same maturity but different coupons lie on the same curve and have different yields, because each blends the spot rates with different weights.

**Slope and forwards.** Write the one-year forward starting at $T$ as $1+f_{T,1}=(1+s_{T+1})^{T+1}/(1+s_T)^{T}$. If $s_{T+1}>s_T$, the denominator is smaller than $(1+s_{T+1})^{T}$, so $f_{T,1}>s_{T+1}>s_T$. Forwards lie above spot rates on an upward-sloping curve, equal them on a flat curve, and lie below them on an inverted curve. A parallel argument, that the par bond's early coupons are discounted at the lower early spot rates, puts the par yield below the spot rate of equal maturity when the curve slopes up, and above it when the curve is inverted.

## A worked example

Cedar Capital's rates desk marks a fictional curve from three bonds that each price at 100 with annual coupons: 2.00% for one year, 3.50% for two years and 4.50% for three years.

Step 1, bootstrap. At one year, $d_1=1/1.02=0.980392$ and $s_1=2.00\%$. The two-year bond pays 3.5 in year one and 103.5 in year two:

$$d_2=\frac{1-0.035\times0.980392}{1.035}=0.933030,\qquad s_2=d_2^{-1/2}-1=3.5266\%$$

The three-year bond pays 4.5, 4.5 and 104.5:

$$d_3=\frac{1-0.045\times(0.980392+0.933030)}{1.045}=0.874542,\qquad s_3=d_3^{-1/3}-1=4.5699\%$$

Rebuilding the par yield from the discount factors, $(1-d_3)/(d_1+d_2+d_3)=4.5\%$, confirms the algebra. Note that $s_3=4.5699\%$ sits above the 4.50% par yield, as it must on an upward curve.

Step 2, forwards, computed at full precision:

$$f_{1,1}=\frac{(1+s_2)^{2}}{1+s_1}-1=5.0761\%,\qquad f_{2,1}=\frac{(1+s_3)^{3}}{(1+s_2)^{2}}-1=6.6879\%$$

The general form with $B=2$ gives the two-year rate that starts in a year, $f_{1,2}=\left[(1+s_3)^{3}/(1+s_1)\right]^{1/2}-1=5.8790\%$. Each forward lies above the spot rate for its end date.

Step 3, how noise grows. Raise only the three-year par yield by one basis point. The three-year spot rate moves by 1.063 basis points, but the 2y1y forward moves by 3.255. A forward is a ratio of two compounded spot factors, and the exponent magnifies an error in the longer one: from $f_{T-1,1}\approx T\,s_T-(T-1)\,s_{T-1}$, an error in $s_T$ is multiplied by about $T$.

Step 4, price off the curve. Take a three-year bond with a 7 annual coupon per 100 of face, well above the 4.50% par coupon:

$$P=7(0.980392)+7(0.933030)+107(0.874542)=106.9699$$

Step 5, the one-yield shortcut. Discount every payment at the three-year par yield, 4.50%, and the price is 106.8724, which is 0.0975 per 100 below the curve value. The law of one price says the curve value is the right one: if the bond traded at 106.8724 you could buy it and sell its three replicating zeros for a riskless 0.0975 per 100. The shortcut error is systematic. Price is linear in the coupon, so the gap, curve value minus shortcut price, is zero for the 4.50% par bond, positive for higher coupons and negative for lower ones; for a three-year zero-coupon payment it is -0.1755.

Step 6, the bond's own yield. Solving $P=\sum_t CF_t/(1+y)^t$ numerically gives $y=4.4662\%$. Three different "three-year rates" now coexist: the par yield 4.50% (the coupon of a bond priced at par), the spot rate 4.5699% (the rate for a single payment in three years), and this bond's yield 4.4662%, a blend that leans on the early, lower spot rates because its large coupons arrive early.

Step 7, what the yield assumes. Buy at 106.9699 and hold to maturity. Reinvest the year-one coupon at $f_{1,1}$ and then $f_{2,1}$, and the year-two coupon at $f_{2,1}$. The terminal value is 122.3154, and

$$122.3154\times d_3=106.9699=P$$

so the realized return is exactly $s_3=4.5699\%$ a year, not the bond's 4.4662%. If the coupons instead earn only today's one-year rate of 2.00%, the realized return falls to 4.3149%. A yield to maturity of 4.4662% needs coupons that earn 4.4662%. A curve that was flat at that level would deliver it; this upward curve does not.

## Interpretation and failure modes

- **A forward is a break-even rate, not a forecast.** The 6.6879% in Step 2 is a rate you can lock in today for the third year, not the market's expectation of what the one-year rate will be in two years. A forward equals the expected future spot rate only if bondholders demand no compensation for rate risk, which is the pure expectations hypothesis. Fama and Bliss (1987) and Cochrane and Piazzesi (2005) are the standard references for the finding that forward rates forecast excess bond returns, which is usually read as evidence that they carry time-varying premia. Read a forward as a price and an inverted curve as an input to scenario analysis, not as a prediction.
- **Forwards amplify input noise.** Step 3 turned one basis point into three. Quotes have bid-ask spreads and rounding, so desks often fit smooth parametric curves such as Nelson and Siegel (1987) or Svensson (1994), trading a little fit for stable forwards.
- **A curve belongs to a risk class.** A government curve discounts riskless promises. Discounting a corporate bond's promised cash flows with it overstates the bond's price, because credit and liquidity compensation is missing. Add a spread: the z-spread is the constant amount added to every spot rate so that discounted cash flows reproduce the market price.
- **Conventions change the numbers.** Semiannual coupon bonds are quoted on a bond-equivalent basis, so 4.50% means 2.25% per half-year. Day counts and accrued interest enter real prices: the 106.9699 above is a price on a coupon date, when accrued interest is zero, whereas between coupon dates the market quotes a clean price that excludes accrued interest and the discounted value is the full price. Between quoted maturities an interpolation rule must be chosen, for example linear in zero rates or in log discount factors, and forwards inherit its kinks.
- **Check the discount factors.** They should be positive and, unless negative rates are intended, decreasing: a rising $d_t$ implies a negative forward. An inconsistent par-yield input can even produce a negative $d_T$, so test before using the curve.
- **A yield is not a return, and it is not additive.** Comparing the yields of bonds with different coupons compares different blends of the curve. A portfolio's yield is not the average of its bonds' yields. A bond's realized return depends on future reinvestment rates that its yield cannot see.

## Implementation

Keep the discount factors as the stored object, because spot, par and forward rates are all functions of them. Many libraries store continuously compounded zero rates $z_t=-\ln(d_t)/t$ instead, for which the forward is simply $f_{A,B}=\big((A+B)z_{A+B}-Az_A\big)/B$. For many pillars, build the lower-triangular par-yield system and solve it with `numpy.linalg.solve`, or loop in maturity order as the worksheet does. Solve a yield with `scipy.optimize.brentq` over a bracket such as -0.5 to 1.0, which is safe because price falls monotonically as the yield rises. Between pillars, interpolate log discount factors with `numpy.interp` as a transparent baseline, and fit a smooth family such as Nelson-Siegel-Svensson with `scipy.optimize.least_squares` on observed prices when stable forwards matter.

In production, QuantLib builds piecewise curves from deposit, bond and swap helpers (for example `PiecewiseLogLinearDiscount` fed by `FixedRateBondHelper` objects) and returns zero and forward rates under a stated compounding and day count through the curve's `zeroRate` and `forwardRate` methods. Reproduce one tenor by hand as a test, as the worksheet does. For government bonds, compare against a published fitted curve such as the Gürkaynak, Sack and Wright (2007) Treasury curve that the Federal Reserve Board publishes. Report every curve-derived number with its compounding convention, day count, interpolation rule and valuation date.""",
            'd_t=(1+s_t)^{-t},\\qquad f_{A,B}=\\left[\\frac{(1+s_{A+B})^{A+B}}{(1+s_A)^{A}}\\right]^{1/B}-1,\\qquad d_T=\\frac{1-y_T\\sum_{t<T}d_t}{1+y_T}',
            r"""# Spot curve from par yields, implied forwards, and one coupon bond priced two ways.
# Par yields are for annual-coupon bonds priced at 100 (fictional desk marks).

def bootstrap(p1, p2, p3):
    # A par bond satisfies p * (d1 + ... + dT) + dT = 1, so solve in maturity order.
    a = 1 / (1 + p1)
    b = (1 - p2 * a) / (1 + p2)
    c = (1 - p3 * (a + b)) / (1 + p3)
    return [a, b, c]

par1 = 0.02
par2 = 0.035
par3 = 0.045
d = bootstrap(par1, par2, par3)
print("Discount factor 1y:", round(d[0], 6))
print("Discount factor 2y:", round(d[1], 6))
print("Discount factor 3y:", round(d[2], 6))

# Spot rates from d_t = (1 + s_t) ** -t
s1 = d[0] ** (-1) - 1
s2 = d[1] ** (-1 / 2) - 1
s3 = d[2] ** (-1 / 3) - 1
print("Spot rate 1y percent:", round(s1 * 100, 4))
print("Spot rate 2y percent:", round(s2 * 100, 4))
print("Spot rate 3y percent:", round(s3 * 100, 4))
par_check = (1 - d[2]) / (d[0] + d[1] + d[2])
print("Par yield recovered at 3y percent:", round(par_check * 100, 4))

# Implied forwards: (1 + s_T) ** T = (1 + s_A) ** A * (1 + f) ** (T - A)
f11 = (1 + s2) ** 2 / (1 + s1) - 1
f21 = (1 + s3) ** 3 / (1 + s2) ** 2 - 1
f12 = ((1 + s3) ** 3 / (1 + s1)) ** (1 / 2) - 1
print("Forward 1y1y percent:", round(f11 * 100, 4))
print("Forward 2y1y percent:", round(f21 * 100, 4))
print("Forward 1y2y percent:", round(f12 * 100, 4))

# Noise amplification: move only the 3y par yield by 1 basis point.
d_up = bootstrap(par1, par2, par3 + 0.0001)
s3_up = d_up[2] ** (-1 / 3) - 1
f21_up = (1 + s3_up) ** 3 / (1 + s2) ** 2 - 1
print("Spot 3y change for +1 bp par yield, bp:", round((s3_up - s3) * 10000, 3))
print("Forward 2y1y change for +1 bp par yield, bp:", round((f21_up - f21) * 10000, 3))

# An off-market bond: 3 years, annual coupon 7 on 100 face.
def price_at(rate, cpn):
    return cpn / (1 + rate) + cpn / (1 + rate) ** 2 + (100 + cpn) / (1 + rate) ** 3

coupon = 7.0
price_curve = coupon * d[0] + coupon * d[1] + (100 + coupon) * d[2]
price_flat = price_at(par3, coupon)
print("Bond price off the curve:", round(price_curve, 4))
print("Bond price at the flat 3y par yield:", round(price_flat, 4))
print("Bond pricing gap:", round(price_curve - price_flat, 4))
zero_gap = 100 * d[2] - price_at(par3, 0.0)
print("Zero-coupon pricing gap:", round(zero_gap, 4))

# Yield to maturity by bisection (price falls as the rate rises).
low = 0.0
high = 0.2
for i in range(60):
    mid = (low + high) / 2
    if price_at(mid, coupon) > price_curve:
        low = mid
    else:
        high = mid
ytm = (low + high) / 2
print("Bond yield to maturity percent:", round(ytm * 100, 4))

# Hold to maturity: what do the coupons earn when reinvested?
tv_forward = coupon * (1 + f11) * (1 + f21) + coupon * (1 + f21) + 100 + coupon
tv_short = coupon * (1 + s1) ** 2 + coupon * (1 + s1) + 100 + coupon
print("Forward-reinvested terminal value:", round(tv_forward, 4))
print("Terminal value times 3y discount factor:", round(tv_forward * d[2], 4))
print("Realized yield, forward reinvestment percent:", round(((tv_forward / price_curve) ** (1 / 3) - 1) * 100, 4))
print("Realized yield, reinvested at 1y spot percent:", round(((tv_short / price_curve) ** (1 / 3) - 1) * 100, 4))""",
            "A second fictional curve is inverted. The desk marks annual-coupon par yields of 5.00% for one year, 4.50% for two years and 4.00% for three years. Bootstrap the discount factors and spot rates, derive the 1y1y, 2y1y and 1y2y forwards, and price a three-year bond with a 2.00% annual coupon both off the curve and at one flat yield equal to the three-year par yield. Then find its yield to maturity, and compare the realized return when its coupons are reinvested at the implied forwards with the return when they earn today's one-year spot rate. Which of the two beats the yield to maturity, and why is the pattern the reverse of the upward-curve case in the lesson?",
            "Bootstrapping gives d1 = 1/1.05 = 0.952381, d2 = (1 - 0.045 x 0.952381)/1.045 = 0.915926 and d3 = (1 - 0.04 x (0.952381 + 0.915926))/1.04 = 0.889680. The spot rates are s1 = 5.0000%, s2 = 0.915926^(-1/2) - 1 = 4.4888% and s3 = 0.889680^(-1/3) - 1 = 3.9733%. The forwards are 1y1y = 1.044888^2/1.05 - 1 = 3.9801%, 2y1y = 1.039733^3/1.044888^2 - 1 = 2.9500% and 1y2y = (1.039733^3/1.05)^(1/2) - 1 = 3.4638%. Each lies below the spot rate for its end date, as an inverted curve requires. Off the curve the bond is worth 2(0.952381) + 2(0.915926) + 102(0.889680) = 94.4840. At one flat 4.00% it is worth 94.4498, so the curve value is 0.0342 higher; for a three-year zero the gap is +0.0684, the reverse of the upward-curve case because s3 is now below the par yield. The bond's yield to maturity is 3.9872%. Reinvesting the coupons at the implied forwards gives a terminal value of 106.2000, and 106.2000 x 0.889680 = 94.4840, so the realized return is exactly s3 = 3.9733%, below the yield. Reinvesting at today's 5.00% gives a terminal value of 106.3050 and a realized return of 4.0076%, above the yield. The pattern reverses because forwards now lie below today's one-year rate. The yield assumes the coupons earn 3.9872%; at the implied forwards they earn 3.98% and then 2.95%, which is less, so the realized return falls short of the yield, and only if the short rate stays near 5.00% do the coupons earn more than the yield assumes. As in the lesson, the forward-reinvestment return is the spot rate, not the yield; the two coincide for every coupon only on a flat curve.",
            [
                q('Spot rates are 3.0% for one year and 4.0% for two years, both annually compounded. What is the 1y1y implied forward rate?', ['5.01%', '4.00%', '3.50%'], 0, 'No arbitrage requires (1.04)^2 = (1.03)(1 + f), so 1 + f = 1.0816 / 1.03 = 1.05010 and f = 5.01%. The 3.50% option averages the two spot rates and the 4.00% option is the two-year spot rate itself. The forward must exceed both because the curve slopes upward.'),
                q("A bond is bought at the price implied by today's spot curve and held to maturity, with every coupon reinvested at the one-year forward rates implied by that same curve. Its realized annual return equals:", ['Its yield to maturity', "The spot rate for the bond's maturity", "The par yield for the bond's maturity"], 1, 'Reinvesting at the implied forwards compounds each coupon exactly as the spot curve prices it, so terminal value times d_T equals the purchase price and the realized return is (1/d_T)^(1/T) - 1 = s_T. For a coupon bond on a sloped curve the yield to maturity differs from it, because the yield assumes reinvestment at the yield itself.'),
                q('Fictional par yields with annual coupons are 5.0% for one year and 4.0% for two years. What is the implied 1y1y forward rate, and what does it show?', ['4.50%, the average of the two par yields, so the forward lies between them', '4.00%, the two-year par yield, so the forward equals the two-year rate', '2.97%, below the two-year spot rate of 3.98%, which shows an inverted curve'], 2, 'Bootstrap first: d1 = 1/1.05 = 0.952381 and d2 = (1 - 0.04 x 0.952381)/1.04 = 0.924908, so s2 = d2^(-1/2) - 1 = 3.98%. The forward is d1/d2 - 1 = 2.97%, below s2 because the curve slopes down. The other options use par yields where spot rates are required.'),
            ],
        ),
    ),
    (
        '2.11',
        (
            '2.34',
            4,
            'Monte Carlo error and variance reduction',
            'Estimate Monte Carlo standard error and cut it with antithetic and control variates, using recorded draws so the result can be reproduced.',
            r"""## The analytical question

Lesson 2.11 introduced Monte Carlo as an average of simulated outcomes and stated that its error shrinks like $1/\sqrt{M}$. This lesson makes that error precise, estimates it from the same draws that produce the answer, and then reduces it by changing the estimator, not the model.

Let $Y_1,\dots,Y_N$ be independent simulated payoffs, discounted to today, with mean $\mu$ (the value sought) and variance $\sigma^2$. The estimator, its variance and its estimated standard error are

$$\hat\mu_N=\frac{1}{N}\sum_{i=1}^{N}Y_i,\qquad \operatorname{Var}(\hat\mu_N)=\frac{\sigma^{2}}{N},\qquad \widehat{\text{SE}}=\frac{s}{\sqrt{N}}$$

where $s$ is the sample standard deviation with divisor $N-1$. The estimator is unbiased and, by the central limit theorem, approximately normal for large $N$. To reach a target standard error $\varepsilon$ the run needs $N=(s/\varepsilon)^{2}$ draws. This is the square law of Lesson 2.29's sample-size formula again: halving the error costs four times the draws, and one more correct decimal digit costs a hundred times. The standard error measures sampling noise only. It says nothing about a wrong model, a coarse time grid or mistaken parameters.

Draws are the expensive way to buy accuracy. The cheaper lever is to lower the variance of what is averaged while keeping its mean. Judge any such method by variance multiplied by computing cost: halving the variance at twice the cost gains nothing.

**Antithetic variates.** Use each normal draw twice, as $Z$ and as $-Z$, which has the same distribution. For a payoff $f(Z)$ the pair average has

$$\operatorname{Var}\!\Big(\tfrac{1}{2}\big[f(Z)+f(-Z)\big]\Big)=\frac{\sigma^{2}}{2}\,(1+\rho_A),\qquad \rho_A=\operatorname{Corr}\big(f(Z),f(-Z)\big)$$

Two independent draws would give $\sigma^{2}/2$ for the same two evaluations, so pairing multiplies the variance by $1+\rho_A$. If $f$ is monotone, $f(Z)$ is non-decreasing and $f(-Z)$ is non-increasing in the same variable, so $\rho_A\le 0$ by Chebyshev's covariance inequality and pairing never loses. If $f$ is not monotone, $\rho_A$ can be positive. For $f(z)=z^{2}$ the two legs are identical, $\rho_A=1$, and each pair buys one draw's information for two evaluations.

**Control variates.** Let $X$ be computed from the same draws, with a mean $\mu_X$ known exactly. For any constant $c$ the estimator $\hat\mu_c=\bar Y+c(\bar X-\mu_X)$ is unbiased, because $\bar X-\mu_X$ has mean zero. Its variance per draw is $\sigma_Y^{2}+c^{2}\sigma_X^{2}+2c\,\sigma_{XY}$, which is smallest at

$$c^{*}=-\frac{\operatorname{Cov}(Y,X)}{\operatorname{Var}(X)},\qquad \operatorname{Var}_{\min}=(1-\rho^{2})\operatorname{Var}(Y),\qquad \rho=\operatorname{Corr}(Y,X)$$

The gain depends only on $\rho^{2}$: $\rho=0.9$ leaves 19% of the variance, $\rho=0.5$ removes only a quarter, and the sign of $\rho$ does not matter. Equivalently, $-c^{*}$ is the slope of the regression of $Y$ on $X$, and the adjusted payoff is the regression residual plus a constant. In option pricing the discounted terminal price is the natural control, because its mean is the initial price under the model's no-arbitrage drift. Kemna and Vorst (1990) controlled the arithmetic-average Asian option with the geometric-average one, which has a closed-form price.

**Reproducibility.** A simulated number can be reproduced only if its random inputs are recorded. A seed fixes the draws of one generator, but NumPy's compatibility policy promises identical streams only for the same bit generator, seed, call sequence, NumPy build, environment and machine, and lets the newer `Generator` change its streams in feature releases; only the legacy `RandomState` is frozen. Record the seed, the library version, $N$, and either the draws or a hash of them. Reuse the same draws across the estimators or scenarios being compared (common random numbers) so that differences reflect the method, not luck. Estimates built on shared draws are correlated, though, so they are not independent replications of one another.

## A worked example

Cedar Capital's analyst desk values a fictional capped-return note that pays, after one year, the gain of a reference price above 100, capped at 20:

$$Y=e^{-rT}\min\{\max(S_T-100,\,0),\,20\}$$

The model is lognormal, $S_T=S_0\exp\{(r-\tfrac{1}{2}\sigma^{2})T+\sigma\sqrt{T}\,Z\}$, with $S_0=100$, $r=0.03$, $\sigma=0.25$ and $T=1$. The guided runtime has no random module, so ten standard-normal draws are recorded and stated as given, and every estimator below reuses them:

$$z=(-0.802,\,-1.324,\,-0.248,\,0.420,\,1.136,\,0.110,\,-0.553,\,-0.785,\,0.749,\,1.635)$$

They sum to 0.338, a cheap integrity check on the list. The payoff is zero for $z$ below 0.005, grows with the price until $z=0.734$, and is flat at the discounted cap, 19.409, beyond that.

Step 1, plain. The ten payoffs are 0, 0, 0, 10.609, 19.409, 2.581, 0, 0, 19.409 and 19.409. Their mean is 7.1417 and their sample standard deviation is 9.0633, so $\widehat{\text{SE}}=9.0633/\sqrt{10}=2.8661$.

Step 2, antithetic. Pair draws one to five with their mirror images: five pairs, ten payoff evaluations, the same cost as Step 1. Because the payoff is zero for every draw below 0.005, a draw and its mirror image cannot both pay, so each pair has one leg at zero. The pair averages are 9.704, 9.704, 3.039, 5.305 and 9.704, with mean 7.4914 and standard error 1.4017. At equal cost the antithetic variance is 0.2392 of the plain variance.

Step 3, control variate. Take $X=e^{-rT}S_T$, whose mean is $S_0=100$ under the model. In the ten draws $\bar X=100.2864$, close to its known mean but not equal to it. The sample gives $\hat c=-0.3424$ and $\hat\rho=0.9221$, so $1-\hat\rho^{2}=0.1497$. The adjusted payoffs $Y+\hat c\,(X-100)$ have mean 7.0436, so the adjustment $\hat c\,(\bar X-100)$ moves the estimate by -0.0981: it cancels part of the sampling error that the draws left in $\bar X$. The standard error is 1.1091, and the variance of the adjusted payoffs is 0.1497 times the plain variance, which is exactly $1-\hat\rho^{2}$ because $\hat c$ is the least-squares coefficient. That standard error treats $\hat c$ as fixed, which is slightly optimistic with ten draws.

Step 4, benchmark. The note is a call spread, so Black-Scholes gives its exact value, 6.885. The errors are +0.26 for the plain estimate, +0.61 for the antithetic one and +0.16 for the control variate. Each lies within one standard error of its own estimate, yet the antithetic error is the largest although its standard error is about half the plain one. A standard error describes how an estimator spreads across repeated runs; any single run can land anywhere inside that spread.

Step 5, cost. Taking each method's ten-draw spread at face value, a standard error of 0.1 needs about 8,215 plain draws, 1,966 antithetic evaluations, or 1,231 controlled draws. These projections inherit the noise of a ten-draw standard deviation, so read them as orders of magnitude.

## Interpretation and failure modes

- **Ten draws are far too few for a standard error to be trusted.** A standard deviation estimated from ten values is uncertain by roughly a quarter even for normal data, and this payoff mixes two point masses with a continuous stretch, so a 95% interval of plus or minus 1.96 standard errors would not reliably have 95% coverage. Verify a claimed standard error by replication: run many independent batches and check that the spread of the batch estimates matches it.
- **A standard error is not one run's error.** Step 4 shows a larger error under the smaller standard error. Report the estimate with its standard error, the method and the number of payoff evaluations, not the closest-looking run.
- **Antithetic pairing needs monotone payoffs.** For a straddle or a squared-return payoff, the legs at $z$ and $-z$ are both large when $|z|$ is large, $\rho_A>0$, and the pair costs two evaluations for less than two draws' information. The assignment for this lesson runs that case.
- **A control variate needs a mean that is exactly known under the simulated model.** If the control is computed from a discretized path but its mean comes from the continuous model, the adjustment adds a bias the standard error does not show. Estimating $c$ from the same draws also makes the estimator slightly biased, by an amount of order $1/N$, and makes $s_w/\sqrt{N}$ slightly optimistic, because the residual has $N-2$ degrees of freedom. Estimate $c$ on a pilot batch and then fix it, or accept the effect at production sizes.
- **Variance reduction repairs sampling noise only.** It leaves the lognormal assumption, parameter error and time-discretization bias exactly where they were.
- **A seed is not a tuning parameter.** Choosing a seed after seeing the answer is a researcher degree of freedom. Fix the seed or the recorded draws before the run.

## Implementation

In NumPy, `rng = np.random.default_rng(seed)` and `z = rng.standard_normal(n)` generate draws, and `y.std(ddof=1) / np.sqrt(n)` is the standard error. The antithetic estimator averages `payoff(z)` and `payoff(-z)` and takes the standard deviation of those pair averages. For the control variate, read the covariance matrix from `np.cov(y, x)` and divide the off-diagonal entry by the variance entry, or take the slope from `np.polyfit(x, y, 1)` and negate it. Do not mix `np.cov` with `np.var`: `np.cov` divides by $N-1$ while `np.var` divides by $N$ unless `ddof=1` is passed, which inflates $c^{*}$ by $N/(N-1)$.

For parallel workers, draw child seeds with `np.random.SeedSequence(entropy).spawn(k)` rather than adding the worker number to a seed. The same seed with a different batch size can give a different stream: NumPy documents that calling `rng.random()` five times is not guaranteed to match `rng.random(5)`. Use `scipy.stats.norm.cdf` for closed-form benchmarks. Randomized quasi-Monte Carlo, with `scipy.stats.qmc.Sobol(d, scramble=True)` and `norm.ppf`, is the next step for reasonably smooth payoffs. Log with every reported value the estimate, standard error, method, $N$, number of payoff evaluations, seed or entropy, library versions and a hash of the draws, for example `hashlib.sha256(z.tobytes()).hexdigest()`.""",
            '\\widehat{\\text{SE}}=\\frac{s}{\\sqrt{N}},\\qquad \\operatorname{Var}_{\\text{pair}}=\\frac{\\sigma^{2}}{2}(1+\\rho_A),\\qquad c^{*}=-\\frac{\\operatorname{Cov}(Y,X)}{\\operatorname{Var}(X)},\\qquad \\operatorname{Var}_{\\min}=(1-\\rho^{2})\\operatorname{Var}(Y)',
            r"""# Plain, antithetic and control-variate Monte Carlo for a capped-return contract.
# The guided runtime has no random module, so the ten standard-normal draws below are
# recorded once, stated as given, and reused by every estimator.
from math import ceil, exp, log, sqrt

# The guided runtime has no erf, so the normal CDF uses the Abramowitz and
# Stegun 26.2.17 approximation, whose published error bound is 7.5e-8.
def phi(x):
    sign = 1.0
    zz = x
    if zz < 0:
        sign = -1.0
        zz = -zz
    t = 1.0 / (1.0 + 0.2316419 * zz)
    poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    tail = 0.3989422804014327 * exp(-0.5 * zz * zz) * poly
    return 0.5 + sign * (0.5 - tail)

s0 = 100.0
strike = 100.0
cap = 20.0
rate = 0.03
vol = 0.25
years = 1.0
disc = exp(-rate * years)

z = [-0.802, -1.324, -0.248, 0.42, 1.136, 0.11, -0.553, -0.785, 0.749, 1.635]
n = len(z)
print("Sum of recorded draws:", round(sum(z), 3))

# The payoff is zero below low_z, linear up to cap_z, and flat at the discounted cap beyond.
low_z = (log(strike / s0) - (rate - 0.5 * vol * vol) * years) / (vol * sqrt(years))
cap_z = (log((strike + cap) / s0) - (rate - 0.5 * vol * vol) * years) / (vol * sqrt(years))
print("Payoff starts above z:", round(low_z, 3))
print("Payoff reaches the cap at z:", round(cap_z, 3))

def terminal(zz):
    return s0 * exp((rate - 0.5 * vol * vol) * years + vol * sqrt(years) * zz)

def payoff(zz):
    gain = terminal(zz) - strike
    if gain < 0:
        gain = 0.0
    if gain > cap:
        gain = cap
    return disc * gain

def sample_sd(total, total_sq, count):
    return sqrt((total_sq - total * total / count) / (count - 1))

# Plain estimator: average the ten discounted payoffs.
sum_y = 0.0
sum_yy = 0.0
for i in range(n):
    y = payoff(z[i])
    print(f"Payoff draw {i + 1}:", round(y, 3))
    sum_y += y
    sum_yy += y * y
plain = sum_y / n
sd_plain = sample_sd(sum_y, sum_yy, n)
se_plain = sd_plain / sqrt(n)
print("Plain estimate:", round(plain, 4))
print("Plain sample standard deviation:", round(sd_plain, 4))
print("Plain standard error:", round(se_plain, 4))

# Antithetic estimator: five pairs (z, -z) cost the same ten payoff evaluations.
pairs = n // 2
sum_a = 0.0
sum_aa = 0.0
for i in range(pairs):
    a = 0.5 * (payoff(z[i]) + payoff(-z[i]))
    print(f"Pair average {i + 1}:", round(a, 3))
    sum_a += a
    sum_aa += a * a
anti = sum_a / pairs
sd_pair = sample_sd(sum_a, sum_aa, pairs)
se_anti = sd_pair / sqrt(pairs)
print("Antithetic estimate:", round(anti, 4))
print("Antithetic standard error:", round(se_anti, 4))
print("Antithetic variance ratio:", round((se_anti / se_plain) ** 2, 4))

# Control variate: discounted terminal price X has known mean s0.
sum_x = 0.0
sum_xx = 0.0
sum_xy = 0.0
for i in range(n):
    x = disc * terminal(z[i])
    sum_x += x
    sum_xx += x * x
    sum_xy += x * payoff(z[i])
mean_x = sum_x / n
cov_xy = (sum_xy - n * mean_x * plain) / (n - 1)
var_x = (sum_xx - n * mean_x * mean_x) / (n - 1)
coef = -cov_xy / var_x
rho = cov_xy / (sd_plain * sqrt(var_x))
print("Control sample mean:", round(mean_x, 4))
print("Control coefficient:", round(coef, 4))
print("Sample correlation:", round(rho, 4))
print("Variance factor:", round(1 - rho * rho, 4))
sum_w = 0.0
sum_ww = 0.0
for i in range(n):
    w = payoff(z[i]) + coef * (disc * terminal(z[i]) - s0)
    sum_w += w
    sum_ww += w * w
control = sum_w / n
sd_w = sample_sd(sum_w, sum_ww, n)
se_control = sd_w / sqrt(n)
print("Control variate estimate:", round(control, 4))
print("Control variate standard error:", round(se_control, 4))
print("Control adjustment:", round(control - plain, 4))
print("Control variance ratio:", round((se_control / se_plain) ** 2, 4))

# Benchmark: the capped call is a call spread, so Black-Scholes gives the exact value.
def call_price(k):
    d1 = (log(s0 / k) + (rate + 0.5 * vol * vol) * years) / (vol * sqrt(years))
    d2 = d1 - vol * sqrt(years)
    return s0 * phi(d1) - k * exp(-rate * years) * phi(d2)

exact = call_price(strike) - call_price(strike + cap)
print("Exact price:", round(exact, 3))
print("Plain error:", round(plain - exact, 2))
print("Antithetic error:", round(anti - exact, 2))
print("Control variate error:", round(control - exact, 2))

# Draws needed for a standard error of 0.1, taking the ten-draw spreads as given.
target = 0.1
print("Draws for standard error 0.1, plain:", ceil((sd_plain / target) ** 2))
print("Draws for standard error 0.1, antithetic evaluations:", 2 * ceil((sd_pair / target) ** 2))
print("Draws for standard error 0.1, control variate:", ceil((sd_w / target) ** 2))""",
            "Replace the capped note with an at-the-money straddle, Y = exp(-rT) |S_T - 100| with no cap, and keep the same ten recorded draws and the same five antithetic pairs. Report the plain, antithetic and control-variate estimates with their standard errors, the antithetic variance ratio, and the control-variate factor 1 - rho^2. The worksheet's call-spread benchmark no longer applies; the exact straddle price is the Black-Scholes call plus the put from put-call parity, and you can use it to check the errors. Then explain, in terms of the antithetic correlation and the control correlation, which method still helps and which one does not.",
            'With Y = exp(-rT) |S_T - 100| the ten payoffs are 17.730, 27.434, 5.948, 10.609, 31.712, 2.581, 12.636, 17.392, 19.838 and 48.819. The plain estimate is 19.4699 with sample standard deviation 13.6439 and standard error 4.3146. The five pair averages are 19.564, 32.671, 6.013, 10.196 and 27.898, giving an estimate of 19.2681 and a standard error of 5.0606, so the antithetic variance is 1.3757 times the plain variance at equal cost: pairing now loses. The payoff is V-shaped, so f(z) and f(-z) are both large when |z| is large, the antithetic correlation is positive, and a mirror image adds little new information. The control variate finds c = -0.3182 and rho = 0.5692, so the factor is 1 - 0.5692^2 = 0.6760 and the adjusted estimate 19.3787 has standard error 3.5474. That removes about a third of the variance, against 0.1497 for the capped note, because a V-shaped payoff has only a partly linear relation to S_T. The exact straddle price is 11.3485 + 8.3930 = 19.7415, so the errors are -0.27, -0.47 and -0.36, each inside one standard error. A numerical-integration check, not a simulation, gives an equal-cost variance ratio of 1.79 for antithetic pairs and a control factor of 0.80 for the straddle, against 0.32 and 0.25 for the capped note, so the direction seen in the ten draws is not luck. Antithetic variates help monotone payoffs and can hurt others; a control variate helps in proportion to rho squared, here modestly.',
            [
                q('A pricing run with 20,000 independent draws reports a standard error of 0.080. About how many draws are needed to bring the standard error down to 0.020?', ['80,000', '320,000', '40,000'], 1, 'Standard error scales as 1/sqrt(N), so cutting it by a factor of four needs sixteen times the draws: 16 x 20,000 = 320,000. Four times the draws, 80,000, would only halve the error to 0.040.'),
                q('A discounted payoff Y has variance 25. A control X with a known mean has variance 100, and Cov(Y, X) = 40. What are the optimal coefficient and the variance of the controlled payoff per draw?', ['c = 0.4 and variance 9', 'c = -0.4 and variance 16', 'c = -0.4 and variance 9'], 2, 'The optimal coefficient is c* = -Cov(Y, X)/Var(X) = -40/100 = -0.4. The correlation satisfies rho^2 = 40^2/(25 x 100) = 0.64, so the controlled variance is (1 - 0.64) x 25 = 9. The figure 16 is the variance removed, not the variance left, and a positive coefficient would add variance instead of removing it.'),
                q('A desk prices a contract paying the squared standardized return, f(Z) = Z^2, and switches from independent draws to antithetic pairs (Z, -Z) at the same number of payoff evaluations. What happens to the variance of the estimate?', ['It doubles, because Z^2 is identical at Z and -Z, so each pair repeats one payoff', 'It halves, because averaging a draw with its mirror image always cancels noise', 'It is unchanged, because antithetic pairs stay unbiased whatever the payoff'], 0, 'Here f(Z) = f(-Z), so the antithetic correlation is 1 and each pair average equals a single payoff. N pairs use 2N evaluations but have variance sigma^2/N, while 2N independent draws would have variance sigma^2/(2N), so the variance doubles. Antithetic pairing needs a monotone payoff; being unbiased says nothing about variance.'),
            ],
        ),
    ),
    (
        '2.12',
        (
            '2.35',
            5,
            'Shrinkage: Bayesian posterior means and the James–Stein estimator',
            'Pull noisy estimates toward a common centre by precision weighting, and show why the shrunk set has lower total squared error even though every shrunk estimate is biased.',
            r"""## The analytical question

Rank six funds by estimated alpha and the top of the list is where noise is most concentrated. Lessons 2.3, 2.9 and 2.12 treated each estimate alone, with a confidence interval, a single Bayes update and a resampled series. None used the fact that the six funds sit side by side, and that fact is informative: the spread of the cross-section says how much of its width is real, which improves every estimate at once. Lesson 2.31 will return to the same pull toward the mean through a correlation; this lesson derives it from a model and lets the data choose the strength.

**The normal–normal model.** Fund $i$ has a true alpha $\theta_i$ and an estimate $x_i$ with known standard error $\sigma$. The prior states how true alphas are spread across the peer group:

$$x_i \mid \theta_i \sim N(\theta_i,\ \sigma^2), \qquad \theta_i \sim N(\mu_0,\ \tau^2)$$

The funds are **exchangeable**: apart from the data, nothing distinguishes one from another. Multiply the two normal densities and complete the square in $\theta_i$. The posterior is again normal, and **precisions add**:

$$\theta_i \mid x_i \sim N(m_i,\ v), \qquad \frac{1}{v} = \frac{1}{\sigma^2} + \frac{1}{\tau^2}, \qquad m_i = \frac{x_i/\sigma^2 + \mu_0/\tau^2}{1/\sigma^2 + 1/\tau^2}$$

The posterior mean is a **precision-weighted average** of the estimate and the prior mean. With $B = \sigma^2/(\sigma^2+\tau^2)$ the same result reads $m_i = (1-B)\,x_i + B\,\mu_0$ and $v = (1-B)\,\sigma^2$. The share $B$ is how far the estimate travels toward the prior mean. It is near one when the estimate is noisy or the prior tight, and near zero when the estimate is precise or the prior vague. The posterior variance is smaller than $\sigma^2$ by the factor $1-B$, because the prior is extra information.

**Credible and confidence intervals.** The interval $x_i \pm 1.96\,\sigma$ is a statement about a procedure: with $\theta_i$ held fixed, it covers $\theta_i$ in 95% of repeated samples, the meaning Lesson 2.3 gave. The interval $m_i \pm 1.96\sqrt{v}$ is a statement about $\theta_i$ given the data and the prior: the probability that $\theta_i$ lies inside is 95%. It is shorter and is centred on a biased value. Its 95% is an average over funds drawn from the prior, so it holds for a typical fund and fails for one whose true alpha lies far out in the tail of the prior. The two intervals answer different questions.

**Empirical Bayes.** Nobody knows $\mu_0$ and $\tau$. But marginally every $x_i \sim N(\mu_0, \sigma^2+\tau^2)$, so the cross-section is a sample from which the prior can be learned. Let $S = \sum_i (x_i-\bar x)^2$. Then $S/(\sigma^2+\tau^2)$ follows a chi-square law with $N-1$ degrees of freedom. An inverse chi-square variable with $\nu$ degrees of freedom has mean $1/(\nu-2)$, so $E[(N-3)/S] = 1/(\sigma^2+\tau^2)$ and $\hat B = (N-3)\sigma^2/S$ is an unbiased estimate of $B$. Put $\bar x$ in place of $\mu_0$ and $\hat B$ in place of $B$, and the posterior mean becomes the **James–Stein estimator** toward the grand mean:

$$\hat\theta_i = \bar x + \left(1-\frac{(N-3)\,\sigma^2}{S}\right)_{+}(x_i-\bar x)$$

The subscript $+$ floors the factor at zero. When $S < (N-3)\sigma^2$ the cross-section is no wider than noise alone would make it. Without the floor the factor would turn negative and reverse the order of the funds; with it, every estimate collapses to $\bar x$. Shrinking toward a fixed point instead of $\bar x$ gives Stein's original factor with $N-2$ in place of $N-3$. Spending one degree of freedom on the grand mean is what turns $N-2$ into $N-3$. The factor is defined from $N=3$ but equals one there, and the guarantee below needs $N \ge 4$.

**Why bias can win.** Stein (1956) showed that for three or more normal means the raw estimates are inadmissible: another rule has no larger total expected squared error for any true vector and a smaller one for some. James and Stein (1961) gave the explicit rule, Lindley (1962) proposed shrinking toward the grand mean, and Efron and Morris (1973) showed the rule is an empirical Bayes estimator. The mechanism is the bias–variance trade. Shrink every estimate by a common weight $w$ toward a centre $c$ and the expected total squared error is

$$N w^{2}\sigma^{2} + (1-w)^{2} D, \qquad D = \sum_i (\theta_i - c)^2$$

The first term is variance and falls as $w$ falls; the second is squared bias and rises. At $w=1$ the slope in $w$ is $2N\sigma^2 > 0$, so some shrinkage helps whatever the true alphas are. The best weight, $D/(D+N\sigma^2)$, depends on the unknown $D$, and Stein's discovery is that $D$ can be estimated from the same data at a cost small enough to keep the gain. The guarantee holds for the sum. Each shrunk estimate is biased, and a fund whose true alpha lies far from the centre can be made worse off.

## A worked example

A fictional selection committee compares six funds in one peer group. Their estimated annual alphas, in percentage points, are 8.0, 5.0, 3.0, 1.0, −1.0 and −4.0 for funds A to F, each with the same standard error $\sigma = 3.0$ (equal track-record lengths and similar residual volatility). Before looking at the data the committee states a prior: true alphas in this group are centred at $\mu_0 = 0$ with spread $\tau = 3.0$.

Step 1, the cross-section. The grand mean is 2.0, the deviations are 6, 3, 1, −1, −3 and −6, and $S = 92$. If all six true alphas were equal, $Q = S/\sigma^2 = 10.222$ would follow a chi-square law with 5 degrees of freedom, giving a p-value of 0.069. The dispersion is borderline against pure noise, which is the first warning that the shrinkage factor will be imprecise.

Step 2, the posterior under the stated prior. The data precision is $1/9 = 0.1111$ and so is the prior precision, giving a posterior precision of 0.2222. The posterior variance is $v = 4.5$, a standard deviation of 2.121, and the weight on each estimate is 0.5. The posterior means are 4.0, 2.5, 1.5, 0.5, −0.5 and −2.0, each the plain average of the estimate and the prior mean because the two precisions are equal.

Step 3, the two intervals for fund A. The 95% confidence interval is $8.0 \pm 1.96 \times 3.0$, from 2.12 to 13.88, and excludes zero. The credible interval is $4.0 \pm 1.96 \times 2.121$, from −0.16 to 8.16, and includes it. This is not a contradiction: the credible interval has used the prior and the confidence interval has not. Judged by repeated sampling, the credible interval covers a fund of true alpha 0 in 99.4% of samples and a fund of true alpha 8.0 in only 54.2%.

Step 4, James–Stein. Here $(N-3)\sigma^2 = 27$, so the factor is $1 - 27/92 = 0.7065$ and the estimated shrinkage share is $\hat B = 0.2935$. The estimates are 6.239, 4.12, 2.707, 1.293, −0.12 and −2.239. Fund A moves from 8.0 to 6.239 under James–Stein but to 4.0 under the stated prior, because the two use different centres (2.0 against 0) and different strengths (0.2935 against 0.5). The cross-section cannot arbitrate between them. The plug-in moment estimate $\hat\tau^2 = S/(N-1) - \sigma^2 = 9.4$ gives $\hat B = 0.489$, almost exactly the committee's 0.5, whereas the $N-3$ rule gives 0.2935. Dividing by a noisy $S$ overstates $B$ on average, and with six funds the correction is large.

Step 5, accounting for squared error. Suppose the stated prior does describe how true alphas vary. Averaged over it, the expected total squared error is $N\sigma^2 = 54$ for the raw estimates and $N(1-B)\sigma^2 = 27$ for the posterior means, which use that prior. The James–Stein rule must learn the centre and the share from the six estimates, which costs $3B\sigma^2 = 13.5$, so its expected total is 40.5, a quarter below the raw 54. That figure is for the rule without the floor; the floor lowers the error further (Baranchik, 1964).

Step 6, the bias fund by fund. The posterior mean with weight $w = 0.5$ has sampling variance $w^2\sigma^2 = 2.25$ and bias $-(1-w)\theta = -\theta/2$ for a fund of true alpha $\theta$, so its mean squared error is $2.25 + \theta^2/4$, against $\sigma^2 = 9$ for the raw estimate. At $\theta = 2$ it is 3.25. At $\theta = 6$ it is 11.25, worse than the raw 9. The break-even alpha is $\sigma\sqrt{(1+w)/(1-w)} = 5.196$. Shrinkage gives a large gain to funds near the centre and a loss to funds far from it, and the sum comes out ahead.

The ranking does not change, because with one common $\sigma$ the shrinkage is increasing in the estimate. What changes is the size of every claim.

## Interpretation and failure modes

**Exchangeability does the work.** Shrinking six funds toward one centre presumes they are draws from one population. A peer group that mixes equity and commodity strategies, or low-fee and high-fee share classes, is not exchangeable, and its grand mean is a poor target. Shrink within homogeneous groups or toward a regression on fund characteristics. The same applies to analyst forecasts: pull each toward the average of analysts covering the same sector rather than toward the whole market.

**Unequal precision changes the answer.** The James–Stein formula assumes one common $\sigma$. When fund $i$ has its own standard error $\sigma_i$, it gets its own share $B_i = \sigma_i^2/(\sigma_i^2+\tau^2)$, and noisier estimates are pulled further. The order of funds can then change: with $\tau = 3$ and $\mu_0 = 0$, an estimate of 6.0 with $\sigma_i = 2$ has a posterior mean of 4.15, above the 1.6 of an estimate of 8.0 with $\sigma_i = 6$. In that case $\tau^2$ must be estimated by a random-effects method from meta-analysis, such as the DerSimonian–Laird or Paule–Mandel estimators, not by the common-factor formula.

**The prior can be wrong.** When two defensible choices disagree as much as the committee's prior and James–Stein did for fund A, report both and the sensitivity of the conclusion to $\tau$, rather than the one that gives the preferred answer. A normal prior is also light-tailed and over-shrinks a genuinely exceptional fund; priors with heavier tails, or with a point mass at zero, shrink small estimates harder and large ones less.

**A small cross-section makes the factor itself noisy.** The empirical Bayes interval built from $v = (1-\hat B)\sigma^2$ ignores the uncertainty in $\hat B$ and is too narrow. Morris (1983) gives a correction. With six funds, treat any such interval with caution.

**Dependence breaks the derivation.** The theory assumes the $x_i$ are independent given the $\theta_i$. Funds loading on the same factor share estimation error, so estimate the factor exposures first and shrink the alphas afterwards.

**Shrinkage is not a selection rule.** A shrunk estimate is a better estimate of the true alpha, and it removes the optimism that comes from picking the highest raw estimate. It does not say whether the alpha will persist, survive fees or scale, and nothing here is investment advice.

## Implementation

With one common standard error the whole procedure is three lines of NumPy:

```python
xbar, s = x.mean(), ((x - x.mean()) ** 2).sum()
factor = max(0.0, 1 - (x.size - 3) * sigma ** 2 / s)
shrunk = xbar + factor * (x - xbar)
```

With unequal standard errors, estimate $\tau^2$ by random-effects meta-analysis. The function `statsmodels.stats.meta_analysis.combine_effects(effect, variance, method_re="dl")` returns `tau2`, the pooled mean `mean_effect_re` and, through `test_homogeneity()`, the chi-square test used in Step 1. Then form $B_i = \sigma_i^2/(\sigma_i^2+\tau^2)$, the shrunk estimate $(1-B_i)x_i + B_i\bar x_{\text{RE}}$ and its variance $(1-B_i)\sigma_i^2$. With equal standard errors this route gives the plug-in share of Step 4, 0.489, not the James–Stein 0.2935. The call `scipy.stats.norm.interval(0.95, loc=m, scale=sd)` returns a credible interval.

Before trusting a shrinkage rule, simulate: draw true alphas from a stated distribution, add noise with the known $\sigma$, and compare the total squared error of raw and shrunk estimates. That tests that the rule helps, where the argument above says only that it should. Report the raw estimate, the shrunk estimate, the factor and how the prior was chosen side by side, so a reader can undo the shrinkage.""",
            'm_i=(1-B)\\,x_i+B\\,\\mu_0,\\ \\ B=\\frac{\\sigma^{2}}{\\sigma^{2}+\\tau^{2}};\\qquad \\hat\\theta_i=\\bar x+\\Bigl(1-\\frac{(N-3)\\sigma^{2}}{\\sum_j (x_j-\\bar x)^{2}}\\Bigr)_{+}(x_i-\\bar x)',
            r"""from math import sqrt, exp

# The guided runtime has no erf, so the normal CDF uses the Abramowitz and
# Stegun 26.2.17 approximation, whose published error bound is 7.5e-8.
def phi(x):
    sign = 1.0
    z = x
    if z < 0:
        sign = -1.0
        z = -z
    t = 1.0 / (1.0 + 0.2316419 * z)
    poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    tail = 0.3989422804014327 * exp(-0.5 * z * z) * poly
    return 0.5 + sign * (0.5 - tail)

alphas = [8.0, 5.0, 3.0, 1.0, -1.0, -4.0]
names = ["A", "B", "C", "D", "E", "F"]
n = len(alphas)
sigma = 3.0
prior_mean = 0.0
prior_sd = 3.0
z95 = 1.959963985

# Step 1: the cross-section.
grand = sum(alphas) / n
spread = 0.0
for a in alphas:
    spread += (a - grand) ** 2
q_stat = spread / sigma ** 2
# Survival function of a chi-square with 5 degrees of freedom (closed form for odd degrees).
root = sqrt(q_stat)
q_p = 2 * (1 - phi(root)) + 2 * 0.3989422804014327 * exp(-0.5 * q_stat) * (root + root ** 3 / 3)
print("Grand mean:", round(grand, 2))
print("Sum of squared deviations:", round(spread, 2))
print("Heterogeneity statistic Q:", round(q_stat, 3))
print("Heterogeneity p-value:", round(q_p, 3))

# Step 2: posterior under the stated prior; precisions add.
data_precision = 1 / sigma ** 2
prior_precision = 1 / prior_sd ** 2
post_precision = data_precision + prior_precision
post_var = 1 / post_precision
weight = data_precision / post_precision
print("Data precision:", round(data_precision, 4))
print("Prior precision:", round(prior_precision, 4))
print("Posterior precision:", round(post_precision, 4))
print("Weight on each estimate:", round(weight, 4))
print("Posterior variance:", round(post_var, 3))
print("Posterior SD:", round(sqrt(post_var), 3))
for i in range(n):
    post_mean = weight * alphas[i] + (1 - weight) * prior_mean
    print(f"Posterior mean fund {names[i]}:", round(post_mean, 3))

# Step 3: confidence versus credible interval for fund A.
top = alphas[0]
top_mean = weight * top + (1 - weight) * prior_mean
half_conf = z95 * sigma
half_cred = z95 * sqrt(post_var)
print("Confidence interval fund A low:", round(top - half_conf, 2))
print("Confidence interval fund A high:", round(top + half_conf, 2))
print("Credible interval fund A low:", round(top_mean - half_cred, 2))
print("Credible interval fund A high:", round(top_mean + half_cred, 2))

def coverage(theta, w, centre, half, sd):
    # The interval is w*x + (1-w)*centre plus or minus half, with x ~ N(theta, sd^2).
    mid = w * theta + (1 - w) * centre
    scale = w * sd
    return phi((theta + half - mid) / scale) - phi((theta - half - mid) / scale)

print("Credible interval coverage at true alpha 0 percent:", round(100 * coverage(0.0, weight, prior_mean, half_cred, sigma), 1))
print("Credible interval coverage at true alpha 8 percent:", round(100 * coverage(8.0, weight, prior_mean, half_cred, sigma), 1))

# Step 4: James-Stein toward the grand mean, positive-part version.
floor_ss = (n - 3) * sigma ** 2
raw_factor = 1 - floor_ss / spread
factor = max(0.0, raw_factor)
print("Collapse threshold for the sum of squares:", round(floor_ss, 2))
print("James-Stein shrinkage factor:", round(factor, 4))
print("Estimated shrinkage share:", round(1 - factor, 4))
for i in range(n):
    js = grand + factor * (alphas[i] - grand)
    print(f"James-Stein fund {names[i]}:", round(js, 3))
tau2_moment = spread / (n - 1) - sigma ** 2
b_moment = sigma ** 2 / (sigma ** 2 + tau2_moment)
print("Moment estimate of tau squared:", round(tau2_moment, 2))
print("Plug-in shrinkage share:", round(b_moment, 3))

# Step 5: expected total squared error averaged over the stated prior.
b = sigma ** 2 / (sigma ** 2 + prior_sd ** 2)
risk_raw = n * sigma ** 2
risk_bayes = n * (1 - b) * sigma ** 2
risk_js = risk_bayes + 3 * b * sigma ** 2
print("Expected total squared error, raw estimates:", round(risk_raw, 2))
print("Expected total squared error, posterior means:", round(risk_bayes, 2))
print("Expected total squared error, James-Stein:", round(risk_js, 2))
print("Cost of learning the prior:", round(risk_js - risk_bayes, 2))

# Step 6: per-fund mean squared error of the posterior mean, variance plus squared bias.
def posterior_mse(theta, w, centre, sd):
    return (w * sd) ** 2 + ((1 - w) * (theta - centre)) ** 2

print("Variance of the posterior mean over repeated samples:", round((weight * sigma) ** 2, 2))
print("Posterior-mean MSE at true alpha 2:", round(posterior_mse(2.0, weight, prior_mean, sigma), 2))
print("Posterior-mean MSE at true alpha 6:", round(posterior_mse(6.0, weight, prior_mean, sigma), 2))
print("Raw-estimate MSE at any true alpha:", round(sigma ** 2, 2))
print("Break-even true alpha:", round(sigma * sqrt((1 + weight) / (1 - weight)), 3))

# Step 7: unequal precision, each estimate with its own standard error.
def posterior_mean_for(estimate, se, centre, spread_sd):
    share = se ** 2 / (se ** 2 + spread_sd ** 2)
    return (1 - share) * estimate + share * centre

print("Posterior mean, estimate 6 with standard error 2:", round(posterior_mean_for(6.0, 2.0, prior_mean, prior_sd), 2))
print("Posterior mean, estimate 8 with standard error 6:", round(posterior_mean_for(8.0, 6.0, prior_mean, prior_sd), 2))""",
            "Five fictional analysts forecast next year's earnings growth for one sector at 13, 9, 5, 1 and −3 percent, and every forecast carries the same standard error of 4 points. (a) Compute the James–Stein factor and the five shrunk forecasts. (b) A committee states the prior that true growth rates are normal with mean 4 and standard deviation 3. Compute the posterior mean, posterior standard deviation and 95% credible interval for the highest forecast, and the confidence interval it replaces. (c) In three sentences, explain why (a) and (b) pull the top forecast by different amounts and what each relies on.",
            '(a) The grand mean is 5.0 and the deviations are 8, 4, 0, −4 and −8, so S = 64 + 16 + 0 + 16 + 64 = 160. With σ² = 16 and N − 3 = 2, the factor is 1 − 2 × 16 / 160 = 0.80, and the shrunk forecasts are 5 + 0.8 × (8, 4, 0, −4, −8) = 11.4, 8.2, 5.0, 1.8 and −1.4. (b) The prior gives B = 16 / (16 + 9) = 0.64, so the weight on a forecast is 0.36. The posterior mean for the top analyst is 0.36 × 13 + 0.64 × 4 = 7.24, the posterior variance is 0.36 × 16 = 5.76, a standard deviation of 2.40, and the 95% credible interval is 7.24 ± 1.96 × 2.40, from 2.54 to 11.94. The confidence interval it replaces is 13 ± 1.96 × 4, from 5.16 to 20.84. (c) James–Stein removes only 20% of the distance to the grand mean 5.0 because the cross-section is wide: S / (N − 1) = 40 against a noise variance of 16, which implies a true spread of about 24 in variance terms. The stated prior removes 64% of the distance to its own centre of 4 because it claims a spread of only 9 in variance terms, much tighter than the forecasts suggest. James–Stein relies on exchangeable analysts, independent errors and the standard error being correct; the posterior relies on an outside judgement about the centre and spread, so when the two disagree this much both should be reported along with the sensitivity of the answer to the prior spread.',
            [
                q('Eight funds have a sum of squared deviations from their grand mean of S = 70 and a common standard error of 2.0. The James–Stein shrinkage factor applied to each deviation from the grand mean is:', ['0.286', '0.600', '0.714'], 2, 'The factor is 1 − (N − 3)σ² / S = 1 − 5 × 4 / 70 = 1 − 0.2857 = 0.714. The value 0.286 is the share removed, not the factor kept, and 0.600 comes from using N − 1 = 7 in place of N − 3 = 5.'),
                q("A fund's alpha estimate is 6.0 with standard error 2.0. The prior for true alphas is normal with mean 1.0 and standard deviation 1.5. The posterior mean is:", ['3.50', '2.80', '4.20'], 1, 'The weight on the estimate is τ² / (σ² + τ²) = 2.25 / (4 + 2.25) = 0.36, so the posterior mean is 0.36 × 6.0 + 0.64 × 1.0 = 2.80. The value 3.50 averages the two with equal weight, and 4.20 reverses the weights.'),
                q("A desk shrinks twelve analysts' growth forecasts toward the desk average with a James–Stein factor. The analyst whose forecasts have been the most accurate ends up with a larger squared error than before. What does this show?", ['Nothing is inconsistent: the guarantee is for total squared error across the analysts, and an analyst far from the group centre can be hurt by the bias', "The factor was computed wrongly, because correct shrinkage lowers every analyst's error", "The analysts' errors were correlated, which is the only way shrinkage can fail"], 0, 'For one analyst the mean squared error after shrinking is w²σ² + (1 − w)²(θ − c)², which exceeds σ² when the true value θ lies far enough from the centre c. The James–Stein result says the sum over all analysts falls, not that each term does.'),
            ],
        ),
    ),
    (
        '2.29',
        (
            '2.36',
            6,
            'Permutation and rank tests when distributions misbehave',
            'Build an exact p-value by relabelling the data, compare it with a t test and a rank-sum test, and say which assumption each one needs.',
            r"""## The analytical question

Lesson 2.4 tested a mean with a $t$ statistic, Lesson 2.29 asked what that test could detect, and Lesson 2.13 asked what happens when many such tests are run. All three lean on a distributional assumption: the $t$ statistic follows Student's law only if the data are normal, or if the sample is large enough for the central limit theorem to rescue the approximation. Eight monthly excess returns, one of them produced by a takeover bid or a data error, offer neither. A single point controls the sample variance, and the reference distribution can no longer be trusted. This lesson builds tests whose validity rests on something other than the shape of the distribution, and says exactly what that something is.

**Exchangeability and the permutation test.** Suppose the null hypothesis says the label on each observation carries no information, so the joint distribution of the data is unchanged when the labels are reshuffled. Then every relabelling is as likely as the one observed. This is Fisher's (1935) randomisation argument, developed into a general test by Pitman (1937). Take any statistic $T$, evaluate it on every way of splitting the $N = n_1 + n_2$ observations into groups of sizes $n_1$ and $n_2$, and count:

$$p = \frac{\#\{\pi : |T(\pi)| \ge |T_{\text{obs}}|\}}{\binom{N}{n_1}}$$

The observed split is one of the relabellings, so $p$ cannot fall below $1/\binom{N}{n_1}$; with equal group sizes the mirror-image split gives $-T$, so a two-sided $p$ cannot fall below twice that. The test is **exact**: its size does not exceed $\alpha$, at any sample size and for any distribution, provided the labels really are exchangeable under $H_0$. The choice of $T$ governs power, not validity.

When $\binom{N}{n_1}$ is too large to enumerate, draw $B$ random relabellings and count the $k$ at least as extreme as the data. The estimator $\hat p = (1+k)/(1+B)$ counts the observed split as one more draw, so it is never zero and stays valid (Phipson and Smyth, 2010). Its Monte Carlo standard error is about $\sqrt{\hat p(1-\hat p)/B}$.

**Permutation versus bootstrap.** Lesson 2.12's bootstrap resamples with replacement to approximate the sampling distribution of an estimator, and its natural output is a confidence interval. The permutation test reshuffles without replacement to build the null distribution of a statistic, and its output is a p-value that is exact under its null. The null it tests is sharp: the labels carry no information about any observation. That is stronger than 'the means are equal', and the gap matters when the spreads differ.

**Rank tests.** Replace each observation by its rank in the pooled sample and extreme values lose their leverage. The Wilcoxon rank-sum statistic $W$ is the sum of the ranks of group 1, and Mann and Whitney's $U = W - n_1(n_1+1)/2$ counts the pairs in which a group-1 value exceeds a group-2 value. With no ties, under $H_0$:

$$E[W] = \frac{n_1(N+1)}{2}, \qquad \operatorname{Var}(W) = \frac{n_1 n_2 (N+1)}{12}$$

The exact null distribution is the distribution of rank sums over the relabellings. It depends only on $n_1$ and $n_2$, so it can be tabulated once. Ties receive average ranks, which alters it slightly.

What the test asserts needs care. Its null is that the two distributions are identical, which is what the permutation argument requires. Against a pure location shift it is a test of the shift. Against anything else it detects $P(X > Y) \ne \tfrac12$, which is not the same as equal means or equal medians. Two samples of different shape can differ in $P(X>Y)$ with equal medians, and the Brunner–Munzel test, `scipy.stats.brunnermunzel`, allows unequal spread.

**Paired data.** For differences $d_i$, such as fund minus benchmark in month $i$, the **sign test** counts the positive differences $K$ among the $n$ nonzero ones. If the median difference is zero, $K$ is Binomial$(n, \tfrac12)$, a null that needs only independence and discards everything but direction. The **Wilcoxon signed-rank test** ranks $|d_i|$ and sums the ranks of the positive differences into $W^+$, with $E[W^+] = n(n+1)/4$. Its exact null comes from the $2^n$ equally likely sign patterns, which requires one more assumption: $d_i$ is symmetric about zero under $H_0$, so that flipping a sign is a relabelling. It is the one-sample form of the permutation argument.

**Robustness and its price.** A rank statistic sees an observation only through its rank. Moving an outlier from 14.0 to 140.0 changes the $t$ statistic and leaves $W$ untouched. The efficiency price is small: Hodges and Lehmann (1956) showed that the rank-sum test's asymptotic relative efficiency against the $t$ test is $3/\pi \approx 0.955$ under normality and never below 0.864 for any distribution, while under heavy tails it can exceed one by a wide margin.

## A worked example

A fictional desk flags four of eight months with a calendar signal and records the strategy's monthly excess return, in percent. The flag-on months return 1.8, 2.4, 3.1 and 14.0, the last driven by a one-off event. The flag-off months return −0.6, 0.4, 0.9 and 1.5. A rule sets the flag, not a lottery, so exchangeability is an assumption that the rule's timing is unrelated to returns under the null.

Step 1, the means. Flag-on averages 5.325 and flag-off 0.55, a difference of 4.775.

Step 2, the $t$ test. The flag-on standard deviation is 5.808, almost all of it the 14.0, against 0.889 for flag-off. The standard error of the difference is 2.938, so $t = 1.625$ on 6 degrees of freedom, with a two-sided p-value of 0.1552. By this test the null is not rejected.

Step 3, enumerate. There are $\binom{8}{4} = 70$ ways to choose which four months carry the flag. Four nested loops visit each one, compute the difference in means and count the splits at least as extreme as 4.775 in absolute value. Two are: the observed split and its mirror image. The exact p-value is $2/70 = 0.0286$.

Step 4, ranks. The flag-on months hold ranks 5, 6, 7 and 8 of eight, so $W = 26$ and $U = 16$, all 16 pairs. Under the null $E[W] = 18$ and the standard deviation is 3.464. The normal approximation with continuity correction gives $z = (8 - 0.5)/3.464 = 2.165$ and $p = 0.0304$. The same 70 splits give the exact value, again 2 of 70, so $p = 0.0286$. The approximation is close even at four against four. At 5% the permutation test rejects the sharp null that the flag changes nothing about the distribution of returns. Because the spreads differ so much, the evidence for a shift in location is the complete separation of the groups, $U = 16$ of 16, not the difference in means alone.

Step 5, the outlier. Replace 14.0 by 140.0. The $t$ statistic falls to 1.055 and its p-value rises to 0.332, because the standard error grows faster than the mean difference. $W$ stays 26 and the exact p-value stays 0.0286.

Step 6, granularity. With three against three the smallest attainable two-sided p-value is $2/20 = 0.1$, so no outcome can reject at 5%. With four against four it is 0.0286, and with five against five 0.0079. These data sit exactly on the floor, which happens only when the groups do not overlap at all. If a Monte Carlo run drew $B = 9{,}999$ relabellings and 284 were at least as extreme, $\hat p = 285/10{,}000 = 0.0285$ with Monte Carlo standard error 0.0017.

Step 7, paired differences. A fund's monthly returns minus its benchmark's over eight months are 0.9, 0.4, 1.3, −0.2, 0.6, 2.1, 0.7 and 5.8. Seven are positive, and the sign test gives $P(K \ge 7 \text{ or } K \le 1) = 18/256 = 0.0703$. The one negative difference has the smallest rank, 1, so $W^+ = 35$, and 4 of the 256 sign patterns are at least as extreme, giving $p = 0.0156$. The paired $t$ statistic is 2.18, below the 5% critical value of 2.365 for 7 degrees of freedom. The three tests use different parts of the same eight numbers: direction only, direction plus the ordering of sizes, and the sizes themselves, including one very large value. Their verdicts differ for that reason.

A p-value of 0.029 from four months against four is not a discovery. The flag was not randomised, a desk that tries many calendar signals needs Lesson 2.13's correction, and Lesson 2.29 says a sample this small can detect only a very large effect.

## Interpretation and failure modes

**What each test assumes.** The pooled $t$ test assumes independent observations, normality or a large sample, and equal variances, and it tests equality of means. The permutation test assumes exchangeability under the null and tests whatever its statistic measures. The rank-sum test assumes independence and identical distributions under the null and detects $P(X>Y) \ne \tfrac12$. The sign test assumes only independence and tests whether the median difference is zero; the signed-rank test adds symmetry and uses the sizes through their ranks.

**Exact does not mean informative.** The test answers whether relabelling alone could produce a gap this large. It does not size the effect. Report the difference in means or the Hodges–Lehmann shift, and for ranks the share $U/(n_1 n_2)$ of pairs won, which here is the maximum possible.

**Autocorrelation breaks exchangeability.** The permutation distribution describes a world in which order carries no information, and returns are not that world. For a mean over the whole series, shuffling or sign-flipping removes the dependence. With AR(1) autocorrelation $\rho$ the variance of the sample mean is inflated by about $(1+\rho)/(1-\rho)$, an effective sample size of $n(1-\rho)/(1+\rho)$. For $\rho = 0.3$ and $n = 60$ that is 32.3 months, and standard errors are understated by a factor of 1.363; Lesson 2.30 met the same inflation in the Sharpe ratio. A flag that arrives in runs suffers in the same way, because random relabelling scatters the runs. Permute blocks long enough to contain the dependence, as Lesson 2.12 did for the bootstrap, or randomise at the level where assignment was truly random.

**Unequal spread breaks it too.** Two groups with equal means but different variances are not exchangeable, so a permutation test of the mean difference is not an exact test of equal means. Permute a studentised statistic, or use Welch's or the Brunner–Munzel test.

**Discreteness and ties.** Attainable p-values are multiples of $1/\binom{N}{n_1}$. With $n$ nonzero paired differences the smallest two-sided sign-test p-value is $2^{1-n}$, which is 0.0625 for five pairs, so five pairs can never reject at 5%. Ties need average ranks and a corrected null.

**Statistic and design are chosen first.** Picking the statistic after seeing which gives the smaller p-value is the multiple-testing problem of Lesson 2.13 in a different form. Fix the statistic, the sidedness and the labels before looking at the outcomes.

## Implementation

```python
import numpy as np
from scipy import stats
res = stats.permutation_test((on, off), lambda a, b: a.mean() - b.mean(),
                             permutation_type="independent", n_resamples=np.inf)
```

With `n_resamples=np.inf` SciPy enumerates every split and returns the exact p-value; with a finite number it samples, adds the observed split as in $(1+k)/(1+B)$, and takes a seeded generator through `rng` or, in older releases, `random_state`. The functions `stats.mannwhitneyu(on, off, method="exact")`, `stats.wilcoxon(d, method="exact")` and `stats.binomtest(k, n, 0.5)` give the rank-sum, signed-rank and sign tests, and `stats.ttest_ind(on, off, equal_var=False)` is Welch's test. For dependent data there is no off-the-shelf permutation test: resample blocks by hand, or use `arch.bootstrap` with a block length chosen as in Lesson 2.12, and report results at several lengths. Report the statistic, the number of relabellings, the exact p-value and an effect size together, along with how the labels were generated.""",
            'p=\\frac{\\#\\{\\pi:\\,|T(\\pi)|\\ge|T_{\\text{obs}}|\\}}{\\binom{N}{n_1}},\\qquad E[W]=\\frac{n_1(N+1)}{2},\\ \\ \\operatorname{Var}(W)=\\frac{n_1n_2(N+1)}{12}',
            r"""from math import sqrt, exp

# The guided runtime has no erf, so the normal CDF uses the Abramowitz and
# Stegun 26.2.17 approximation, whose published error bound is 7.5e-8.
def phi(x):
    sign = 1.0
    z = x
    if z < 0:
        sign = -1.0
        z = -z
    t = 1.0 / (1.0 + 0.2316419 * z)
    poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + t * 1.330274429))))
    tail = 0.3989422804014327 * exp(-0.5 * z * z) * poly
    return 0.5 + sign * (0.5 - tail)

# Monthly excess returns in percent: the four flag-on months first, then the four flag-off months.
x = [1.8, 2.4, 3.1, 14.0, -0.6, 0.4, 0.9, 1.5]
total = sum(x)

def spread(values, centre):
    ss = 0.0
    for v in values:
        ss += (v - centre) ** 2
    return ss

# Step 1: the observed difference in means.
mean_on = sum(x[0:4]) / 4
mean_off = sum(x[4:8]) / 4
diff = mean_on - mean_off
print("Mean excess return, flag on:", round(mean_on, 3))
print("Mean excess return, flag off:", round(mean_off, 3))
print("Mean difference:", round(diff, 3))

# Step 2: the pooled two-sample t test.
def two_sample_t(values):
    m_on = sum(values[0:4]) / 4
    m_off = sum(values[4:8]) / 4
    pooled_var = (spread(values[0:4], m_on) + spread(values[4:8], m_off)) / 6
    return (m_on - m_off) / sqrt(pooled_var * (1 / 4 + 1 / 4))

# Two-sided p-value of a Student t with 6 degrees of freedom (closed form for even degrees).
def t6_p_value(t):
    u = 6 / (6 + t * t)
    return 1 - (abs(t) / sqrt(6 + t * t)) * (1 + u / 2 + 3 * u * u / 8)

t_stat = two_sample_t(x)
print("Sample SD flag on:", round(sqrt(spread(x[0:4], mean_on) / 3), 3))
print("Sample SD flag off:", round(sqrt(spread(x[4:8], mean_off) / 3), 3))
print("Standard error of the difference:", round(diff / t_stat, 3))
print("Student t statistic:", round(t_stat, 3))
print("Student t p-value:", round(t6_p_value(t_stat), 4))

# Step 3: enumerate every way to choose the four flagged months. Ranks have no ties here.
def rank_of(values, i):
    r = 1
    for v in values:
        if v < values[i]:
            r += 1
    return r

ranks = [rank_of(x, 0), rank_of(x, 1), rank_of(x, 2), rank_of(x, 3), rank_of(x, 4), rank_of(x, 5), rank_of(x, 6), rank_of(x, 7)]
w_obs = ranks[0] + ranks[1] + ranks[2] + ranks[3]
w_centre = 4 * (8 + 1) / 2
splits = 0
extreme_mean = 0
extreme_rank = 0
for i1 in range(0, 5):
    for i2 in range(i1 + 1, 6):
        for i3 in range(i2 + 1, 7):
            for i4 in range(i3 + 1, 8):
                splits += 1
                sum_a = x[i1] + x[i2] + x[i3] + x[i4]
                gap = (sum_a - (total - sum_a)) / 4
                # The small tolerance guards against floating-point round-off on ties with the observed gap.
                if abs(gap) >= abs(diff) - 0.000000001:
                    extreme_mean += 1
                w_split = ranks[i1] + ranks[i2] + ranks[i3] + ranks[i4]
                if abs(w_split - w_centre) >= abs(w_obs - w_centre):
                    extreme_rank += 1
print("Splits enumerated:", splits)
print("Splits with a mean difference at least as extreme:", extreme_mean)
print("Exact permutation p-value:", round(extreme_mean / splits, 4))

# Step 4: the rank-sum statistic, its normal approximation and its exact p-value.
null_sd = sqrt(4 * 4 * (8 + 1) / 12)
z_rank = (abs(w_obs - w_centre) - 0.5) / null_sd
print("Rank sum W for the flag-on months:", w_obs)
print("Mann-Whitney U:", w_obs - 10)
print("Null mean of W:", w_centre)
print("Null SD of W:", round(null_sd, 3))
print("Normal approximation z with continuity correction:", round(z_rank, 3))
print("Normal approximation p-value:", round(2 * (1 - phi(z_rank)), 4))
print("Splits with a rank sum at least as extreme:", extreme_rank)
print("Exact rank-sum p-value:", round(extreme_rank / splits, 4))

# Step 5: make the outlier ten times larger.
y = [1.8, 2.4, 3.1, 140.0, -0.6, 0.4, 0.9, 1.5]
t_big = two_sample_t(y)
w_big = rank_of(y, 0) + rank_of(y, 1) + rank_of(y, 2) + rank_of(y, 3)
print("Student t statistic with the outlier times ten:", round(t_big, 3))
print("Student t p-value with the outlier times ten:", round(t6_p_value(t_big), 3))
print("Rank sum W with the outlier times ten:", w_big)

# Step 6: granularity of exact p-values, and a Monte Carlo p-value.
def choose(n, k):
    c = 1
    for i in range(k):
        c = c * (n - i) // (i + 1)
    return c

mc_p = (1 + 284) / (1 + 9999)
print("Smallest two-sided exact p-value, 3 against 3:", round(2 / choose(6, 3), 4))
print("Smallest two-sided exact p-value, 4 against 4:", round(2 / choose(8, 4), 4))
print("Smallest two-sided exact p-value, 5 against 5:", round(2 / choose(10, 5), 4))
print("Smallest two-sided sign-test p-value, 5 pairs:", 2 / 2 ** 5)
print("Monte Carlo p-value from 284 hits in 9999 draws:", round(mc_p, 4))
print("Monte Carlo standard error:", round(sqrt(mc_p * (1 - mc_p) / 9999), 4))

# Step 7: paired differences, fund minus benchmark. Sign patterns are enumerated as 8-bit numbers.
d = [0.9, 0.4, 1.3, -0.2, 0.6, 2.1, 0.7, 5.8]

def abs_rank(values, i):
    r = 1
    for v in values:
        if abs(v) < abs(values[i]):
            r += 1
    return r

positives = 0
w_plus = 0
for i in range(8):
    if d[i] > 0:
        positives += 1
        w_plus += abs_rank(d, i)
sign_extreme = 0
signed_extreme = 0
for pattern in range(256):
    k = 0
    w = 0
    for j in range(8):
        bit = (pattern // 2 ** j) % 2
        k += bit
        w += bit * (j + 1)
    if abs(k - 4) >= abs(positives - 4):
        sign_extreme += 1
    if abs(w - 18) >= abs(w_plus - 18):
        signed_extreme += 1
mean_d = sum(d) / 8
t_paired = mean_d / (sqrt(spread(d, mean_d) / 7) / sqrt(8))
print("Positive differences:", positives)
print("Sign test p-value:", round(sign_extreme / 256, 4))
print("Signed-rank statistic W plus:", w_plus)
print("Signed-rank exact p-value:", round(signed_extreme / 256, 4))
print("Paired t statistic:", round(t_paired, 2))
# 97.5th percentile of Student t with 7 degrees of freedom, hard-coded from standard tables.
print("Critical t at 7 degrees of freedom:", 2.365)

# Autocorrelation: effective sample size of a mean for an AR(1) series.
rho = 0.3
months = 60
print("Effective sample size at autocorrelation 0.3:", round(months * (1 - rho) / (1 + rho), 1))
print("Standard error understatement factor:", round(sqrt((1 + rho) / (1 - rho)), 3))""",
            "A second desk's eight different months are split by the same calendar flag. The four flag-on months return 1.9, 2.6, 3.3 and 12.4 percent, and the four flag-off months return −1.2, 0.3, 1.1 and 2.9. (a) Compute the difference in means. (b) Enumerate all 70 splits to find the exact two-sided permutation p-value for the difference in means. (c) Compute the rank-sum statistic W for the flag-on months and its exact two-sided p-value. (d) Compute the pooled t statistic. (e) The two exact p-values differ: explain why, and say which you would report and what you would add.",
            '(a) The flag-on months average 5.05 and the flag-off months 0.775, so the difference is 4.275. (b) Of the 70 splits, 6 give a mean difference at least 4.275 in absolute value, so the exact p-value is 6/70 = 0.0857. (c) The pooled ranks put the flag-on months at 4, 5, 7 and 8, so W = 24 and U = 14; under the null E[W] = 18, and 8 of the 70 splits have a rank sum at least 6 from 18, so the exact p-value is 8/70 = 0.1143. (d) The pooled t statistic is 1.638 on 6 degrees of freedom, with a two-sided p-value of 0.1526. (e) The two statistics order the 70 splits differently. The split {1.1, 2.9, 3.3, 12.4} has the same rank sum, 24, as the observed split {1.9, 2.6, 3.3, 12.4}, so the rank test counts it as equally extreme, but its values sum to 19.7 against 20.2, so the mean-based test does not; that split and its mirror image account for the gap between 8/70 and 6/70. Both exact p-values are valid when the labels are exchangeable under the null, and the statistic must be fixed before the data are seen. Report the pre-chosen one, add the other as a sensitivity check, and give an effect size such as the 4.275 difference or the 14 of 16 pairs that the flag-on months win. Neither p-value rejects at 5%, and with four against four the rank-sum test can reject only on complete separation, since the next-smallest p-value after 2/70 is 4/70 = 0.0571.',
            [
                q('Three monthly returns are compared with three others in an exact two-sided permutation test, with no ties. The smallest p-value any outcome can produce is:', ['0.050', '0.100', '0.033'], 1, 'There are C(6,3) = 20 ways to choose the three labelled months. Only the observed split and its mirror image can be the most extreme, so the smallest two-sided p-value is 2/20 = 0.100, and no outcome can reject at 5%.'),
                q('Of ten nonzero paired differences, seven are positive. The exact two-sided sign-test p-value is:', ['0.172', '0.117', '0.344'], 2, 'Under the null the count of positives is Binomial(10, 1/2). P(K ≥ 7) = (120 + 45 + 10 + 1)/1024 = 0.172, and doubling for the other tail gives 0.344. The value 0.172 is one-sided and 0.117 is only P(K = 7).'),
                q("A 60-month series of positively autocorrelated returns is split into months flagged 'after a policy-rate rise', which arrive in runs of several months, and other months. A test that shuffles the flags at random across months will tend to give:", ['p-values that are too small, because shuffling scatters the runs and removes the dependence that makes the real difference more variable', 'p-values that are too large, because ranks discard information about the size of returns', 'exact p-values, because a permutation test needs no assumptions about the data'], 0, 'Exchangeability of the labels fails when the flag comes in runs and the returns are autocorrelated. Random relabelling produces scattered subsets whose mean difference varies less than the run-structured real one, so the reference distribution is too narrow and the p-value too small. The fix is to permute whole blocks.'),
            ],
        ),
    ),
    (
        '2.16',
        (
            '2.37',
            8,
            'Logistic regression for qualitative outcomes',
            'Fit and read a logit model: log-odds, maximum likelihood, odds ratios, marginal effects, likelihood-ratio tests, separation and a cost-based decision threshold.',
            r"""## The analytical question

Lesson 2.15 used qualitative information as a regressor. Credit and event research use it as the outcome: a borrower defaults or does not, a firm beats consensus or does not, a bond is downgraded or is not. With $y_i \in \{0, 1\}$ the object to model is the probability $p_i = \Pr(y_i = 1 \mid x_i)$. Lesson 2.20 graded classifiers from a confusion matrix; this lesson builds the probability model that produces the scores being graded.

**Why the linear probability model fails.** OLS of $y$ on $x$ gives $\hat p = x^{\top}\hat\beta$, which has three defects. Fitted values leave $[0, 1]$ once $x$ is extreme enough. The error variance is $p(1 - p)$, so it changes with $x$ by construction: the conditional heteroskedasticity of Lesson 2.16 is guaranteed, and conventional standard errors are wrong. And the slope is constant, so one more unit of $x$ must move the probability equally at $p = 0.01$ and at $p = 0.50$, which a bounded probability cannot do over a wide range.

**The logit model.** Let a latent score $y_i^{*} = x_i^{\top}\beta + u_i$ drive the outcome, with $y_i = 1$ when $y_i^{*} > 0$ and $u_i$ standard logistic. Then

$$p_i = \Lambda(x_i^{\top}\beta) = \frac{1}{1 + e^{-x_i^{\top}\beta}}, \qquad \ln\frac{p_i}{1 - p_i} = x_i^{\top}\beta$$

The log-odds are unbounded, so a linear index is admissible, and every fitted probability stays inside $(0, 1)$. A normal error gives the probit model, with similar probabilities away from the tails. The logistic error has fixed variance $\pi^2/3$, which pins the scale of the latent score. A regressor that explains part of the latent variation therefore rescales every other coefficient, even when it is uncorrelated with them, so coefficients from models with different regressors are not directly comparable (Mood, 2010).

**Maximum likelihood.** For independent observations the log-likelihood, score and Hessian are

$$\ell(\beta) = \sum_{i=1}^{n}\left[y_i x_i^{\top}\beta - \ln\left(1 + e^{x_i^{\top}\beta}\right)\right], \quad s(\beta) = X^{\top}(y - p), \quad H(\beta) = -X^{\top}WX$$

with $W = \text{diag}\,[p_i(1 - p_i)]$. The equation $s(\beta) = 0$ has no closed form, because $p$ is nonlinear in $\beta$. The Hessian is negative definite when $X$ has full column rank, so $\ell$ is strictly concave and a solution, if one exists, is the unique maximum. Newton–Raphson, which here equals iteratively reweighted least squares, climbs to it:

$$\beta^{(k+1)} = \beta^{(k)} + \left(X^{\top}W^{(k)}X\right)^{-1}X^{\top}\left(y - p^{(k)}\right)$$

At the solution $(X^{\top}\hat WX)^{-1}$ is the estimated covariance matrix, which gives standard errors and Wald statistics $z_j = \hat\beta_j / \widehat{\text{se}}_j$. Two facts help with checking. With an intercept, the first score equation forces $\sum_i \hat p_i = \sum_i y_i$, so fitted probabilities average to the observed rate. And the first Newton step from the intercept-only fit has a slope equal to the linear-probability slope divided by $\bar y(1 - \bar y)$: to first order, logit is a rescaled linear probability model.

**Reading coefficients.** $e^{\beta_j}$ is an odds ratio: one more unit of $x_j$ multiplies the odds $p/(1 - p)$ by $e^{\beta_j}$, whatever the other regressors are. It is not a risk ratio; the two agree only when $p$ is small. The effect on the probability depends on where you stand:

$$\frac{\partial p}{\partial x_j} = \beta_j\,p(1 - p), \qquad \text{AME}_j = \frac{1}{n}\sum_{i=1}^{n}\hat\beta_j\,\hat p_i(1 - \hat p_i)$$

The derivative peaks at $\beta_j/4$ when $p = 0.5$. The average marginal effect (AME) averages it over the sample; for a dummy, use the discrete change $\Lambda(x^{(1)\top}\hat\beta) - \Lambda(x^{(0)\top}\hat\beta)$. The effect at the mean regressor values is a different number, because $p(1 - p)$ is not linear. Delta-method standard errors exist for both.

**Testing and fit.** For $q$ restrictions, Wilks' likelihood-ratio statistic is $\text{LR} = 2(\ell_U - \ell_R) \sim \chi^2_q$ under the null, where $\ell_U$ and $\ell_R$ are the maximised log-likelihoods without and with the restrictions. Against the intercept-only model, whose log-likelihood is $\ell_0 = n[\bar y \ln \bar y + (1 - \bar y)\ln(1 - \bar y)]$, it tests every slope at once, and McFadden's pseudo-$R^2$ is $1 - \ell_U/\ell_0$. It is not a share of variance explained and runs lower than an OLS $R^2$; McFadden's own rule of thumb is that 0.2 to 0.4 is already an excellent fit. The Wald and LR tests agree only asymptotically, and the Wald statistic can shrink as $|\hat\beta|$ grows (Hauck and Donner, 1977), so prefer LR when estimates are large.

**Separation.** If some combination of regressors classifies the sample perfectly (complete separation), or perfectly apart from ties on the boundary (quasi-complete, as with a sector dummy that has no defaults in it), the likelihood keeps rising as coefficients go to infinity. No finite maximum exists (Albert and Anderson, 1984) and Newton–Raphson drifts without converging. Remedies are Firth's (1993) penalised likelihood, an L2 penalty, merging sparse categories, or more data.

**From probability to decision.** Flagging a loan with default probability $p$ costs $(1 - p)C_{FP}$ in expectation and not flagging it costs $p\,C_{FN}$, so flag when $p > p^{*} = C_{FP}/(C_{FP} + C_{FN})$, the threshold of Lesson 2.20. On the log-odds scale the rule is $x^{\top}\hat\beta > \ln(C_{FP}/C_{FN})$. It is only as good as the calibration of $\hat p$.

## A worked example

A credit team at a fictional lender models whether a small-business borrower defaults within twelve months. Leverage is net debt over EBITDA in turns, interest cover is EBIT over interest, and the concentration dummy is 1 when the largest customer exceeds 30% of revenue.

**Teaching sample: the machinery.** Ten loans from a workout book have leverage 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0 and 6.0. The four at 3.0, 4.0, 5.0 and 6.0 defaulted, so $\bar y = 0.4$.

Step 1, the linear probability model. The OLS slope is 0.2078. The line gives a fitted probability of −0.0779 at leverage 1.0 and 1.1688 at leverage 7.0, and neither is a probability.

Step 2, one Newton step from the intercept-only fit $(\ln(0.4/0.6), 0) = (-0.4055, 0)$, where every fitted probability is 0.4 and $\ell = -6.7301$. The leverage sums are $\sum x_i = 33$, $\sum x_i^2 = 132$ and $\sum y_i x_i = 18$. The intercept score vanishes because the fit already averages to the default rate, and the slope score is $18 - 0.4 \times 33 = 4.8$. Every weight $p_i(1 - p_i)$ equals $0.4 \times 0.6 = 0.24$, so

$$s = \begin{pmatrix}0\\4.8\end{pmatrix}, \quad I = 0.24\begin{pmatrix}10 & 33\\33 & 132\end{pmatrix}, \quad \det I = 13.3056, \quad \Delta\beta = I^{-1}s = \begin{pmatrix}-2.8571\\0.8658\end{pmatrix}$$

The updated pair is $\beta^{(1)} = (-3.2626, 0.8658)$ and the log-likelihood rises to −4.454. The new slope is $0.2078/0.24 = 0.8658$, the rescaled linear-probability slope.

Step 3, iterate. The slope goes 0.8658, 1.1813, 1.2808, 1.289 and the log-likelihood −4.454, −4.2724, −4.2618, −4.2618, which is the quadratic convergence Newton–Raphson shows near a maximum. The solution is $\hat\beta = (-4.9236, 1.2891)$ with $\hat\ell = -4.2618$, and the fitted probabilities sum to 4.0, the number of defaults.

Step 4, inference. The inverse information gives a slope standard error of 0.789 and $z = 1.634$, so $z^2 = 2.669$. The likelihood-ratio statistic is $2(-4.2618 + 6.7301) = 4.937$. Against the 5% critical value 3.841 for one degree of freedom, LR rejects and Wald does not.

Step 5, effects. The odds ratio is $e^{1.2891} = 3.629$ per turn. The AME is 0.1762 and the effect at the mean leverage of 3.3 is 0.2887, against a linear-probability slope of 0.2078: three numbers for three different questions.

Step 6, separation. Relabel so the defaults are exactly the loans with leverage 4.0 or more, which a line now separates. After 10 Newton iterations the slope is 27.856 and still climbing (by 4.01 in the last iteration), the log-likelihood is −0.0019, and the Wald statistic has fallen to 0.3024 because the standard error grows faster than the slope.

**Production model: reading a fitted logit.** A model fitted on 1,000 loans with 80 defaults gives

$$\hat\eta = -3.80 + 0.55\,\text{leverage} - 0.35\,\text{cover} + 0.80\,\text{concentrated}$$

Step 7, probabilities. Borrower A has leverage 3.0, cover 4.0 and a concentrated customer base: $\hat\eta = -2.75$ and $\hat p = 0.0601$. Borrower B is identical but at leverage 4.0: $\hat\eta = -2.2$ and $\hat p = 0.0998$.

Step 8, odds ratios and effects. The odds ratios are $e^{0.55} = 1.7333$ for leverage, $e^{-0.35} = 0.7047$ for cover and $e^{0.80} = 2.2255$ for concentration. B's risk ratio against A is 1.6601, below the odds ratio. The marginal effect of leverage at A is $0.55 \times 0.0601 \times 0.9399 = 0.0311$, while the actual move from A to B is 0.0397. Concentration moves A's probability by 0.0322, although its odds ratio of 2.2255 applies to every borrower.

Step 9, tests and fit. With 80 defaults in 1,000 loans, $\ell_0 = -278.7694$. The reported full-model log-likelihood is −241.60, so $\text{LR} = 74.339$ against the 5% critical value 7.815 for three degrees of freedom, and McFadden's $R^2$ is 0.1333. Dropping the concentration dummy gives −244.50 and $\text{LR} = 5.8$: above 3.841, so significant at 5%, and below 6.635, so not at 1%.

Step 10, the decision. A missed default costs 40 units and a wrongly declined sound loan costs 2, so $p^{*} = 2/42 = 0.0476$, which is −2.9957 on the log-odds scale. A's 0.0601 exceeds it: declining costs $0.9399 \times 2 = 1.8798$ in expectation and approving costs $0.0601 \times 40 = 2.4035$, so decline. At the habitual 0.5 cut-off A would be approved.

## Interpretation and failure modes

Odds ratios are not risk ratios. Between A and B the odds ratio of 1.7333 corresponds to a risk ratio of 1.6601, and the overstatement grows with the base rate. Marginal effects belong to a place in the data, not to the model: say which one you report, and average over the population that will be scored.

Likelihood inference is asymptotic. The teaching sample has 4 events for one slope, well under the rough rule of ten events per regressor (Peduzzi and colleagues, 1996), and its Wald and LR tests disagree. The production model has 80 events for three slopes, or 26.7 per regressor. In rare-event samples maximum likelihood can also sharply underestimate event probabilities (King and Zeng, 2001), which feeds straight into thresholds.

The model assumes independent outcomes, a correctly specified linear index and a logistic link. Defaults cluster by sector and by credit cycle, so inverse-information standard errors are optimistic; cluster by sector or period, as Lesson 2.16 argued for dependent errors, with `fit(cov_type="cluster", cov_kwds={"groups": g})`. A misspecified index, such as a leverage effect that flattens above five turns, appears as miscalibration within leverage buckets. Add a spline or squared term and compare the fits by likelihood ratio.

Calibration does not travel. Suppose the 8% default rate of the fitting sample becomes 3% in the book to be scored. If only the base rate changed, slopes may hold but the intercept must shift by $\ln[(0.03/0.97)/(0.08/0.92)] = -1.0338$. A's probability falls to 0.0222, below the threshold 0.0476, and the decision flips. An uncorrected intercept costs money without moving any fit statistic.

A significant coefficient is still an association given the included regressors (Lesson 2.15), not a causal effect. In-sample McFadden $R^2$ rises with every added regressor, so compare specifications out of sample, as in Lesson 2.19.

## Implementation

In statsmodels, `sm.Logit(y, sm.add_constant(X)).fit()` runs Newton–Raphson and returns an object whose attributes match this lesson: `params`, `bse`, `llf` (fitted log-likelihood), `llnull` (intercept-only), `llr` and `llr_pvalue` (the LR test against it) and `prsquared` (McFadden). Exponentiate `params` and `conf_int()` for odds ratios with Wald intervals. `res.get_margeff(at="overall", dummy=True).summary()` gives AMEs with delta-method errors, and `at="mean"` gives effects at the means. For a nested test, fit both models, compute `lr = 2 * (res_u.llf - res_r.llf)` and call `scipy.stats.chi2.sf(lr, q)`. `res.pred_table(threshold)` returns the confusion matrix at any cut-off, and `sm.GLM(y, X, family=sm.families.Binomial())` fits the same model by IRLS. Scikit-learn's `LogisticRegression` applies an L2 penalty by default, so pass `C=np.inf` (`penalty=None` before release 1.8) for the maximum-likelihood fit, and use `sklearn.calibration.calibration_curve` to check predicted probabilities against observed frequencies before trusting a threshold. Under separation statsmodels emits `PerfectSeparationWarning` (older releases raised `PerfectSeparationError`), `res.mle_retvals["converged"]` is False and standard errors are enormous. Treat these as a stop sign, then penalise or merge categories.""",
            '\\ln\\frac{p}{1-p}=x^{\\top}\\beta,\\qquad \\text{LR}=2(\\ell_U-\\ell_R)\\sim\\chi^2_q,\\qquad p^{*}=\\frac{C_{FP}}{C_{FP}+C_{FN}}',
            r"""from math import exp, log, sqrt

# Teaching sample: leverage (net debt / EBITDA) and default within twelve months.
x = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0]
y = [0, 0, 0, 0, 1, 0, 1, 0, 1, 1]
n = len(x)
xbar = sum(x) / n
ybar = sum(y) / n

# Step 1: the linear probability model.
sxx = 0.0
sxy = 0.0
sum_xx = 0.0
sum_xy = 0.0
for i in range(n):
    sxx += (x[i] - xbar) ** 2
    sxy += (x[i] - xbar) * (y[i] - ybar)
    sum_xx += x[i] * x[i]
    sum_xy += x[i] * y[i]
lpm_slope = sxy / sxx
lpm_icpt = ybar - lpm_slope * xbar
print("LPM slope:", round(lpm_slope, 4))
print("LPM fitted probability at leverage 1.0:", round(lpm_icpt + lpm_slope * 1.0, 4))
print("LPM fitted probability at leverage 7.0:", round(lpm_icpt + lpm_slope * 7.0, 4))

# Log-likelihood of a coefficient pair for any label list.
def loglik(b0, b1, labels):
    total = 0.0
    for i in range(n):
        eta = b0 + b1 * x[i]
        total += labels[i] * eta - log(1 + exp(eta))
    return total

# One Newton-Raphson step. Returns the updated pair, the slope score,
# the information determinant and the information entries I00 and I11.
def newton(b0, b1, labels):
    s0 = 0.0
    s1 = 0.0
    i00 = 0.0
    i01 = 0.0
    i11 = 0.0
    for i in range(n):
        p = 1 / (1 + exp(-(b0 + b1 * x[i])))
        w = p * (1 - p)
        s0 += labels[i] - p
        s1 += (labels[i] - p) * x[i]
        i00 += w
        i01 += w * x[i]
        i11 += w * x[i] * x[i]
    det = i00 * i11 - i01 * i01
    return [b0 + (i11 * s0 - i01 * s1) / det, b1 + (i00 * s1 - i01 * s0) / det, s1, det, i00, i11]

# Steps 2 and 3: Newton-Raphson from the intercept-only fit.
start0 = log(ybar / (1 - ybar))
b0 = start0
b1 = 0.0
ll_null = loglik(b0, b1, y)
print("Intercept-only start:", round(start0, 4))
print("Log-likelihood at the intercept-only start:", round(ll_null, 4))
print("Mean leverage:", round(xbar, 4))
print("Sum of leverage:", sum(x))
print("Sum of squared leverage:", sum_xx)
print("Sum of leverage over defaults:", sum_xy)
for k in range(1, 7):
    r = newton(b0, b1, y)
    if k == 1:
        print("Score for slope at the start:", round(r[2], 4))
        print("Information determinant at the start:", round(r[3], 4))
        print("Newton step, intercept:", round(r[0] - b0, 4))
        print("Newton step, slope:", round(r[1] - b1, 4))
        print("LPM slope divided by ybar(1 - ybar):", round(lpm_slope / (ybar * (1 - ybar)), 4))
        print("Step 1 intercept:", round(r[0], 4))
    b0 = r[0]
    b1 = r[1]
    if k < 5:
        print("Iteration", k, "slope:", round(b1, 4))
        print("Iteration", k, "log-likelihood:", round(loglik(b0, b1, y), 4))

# Step 4: inference at the solution.
final = newton(b0, b1, y)
se_slope = sqrt(final[4] / final[3])
z = b1 / se_slope
ll_hat = loglik(b0, b1, y)
lr = 2 * (ll_hat - ll_null)
print("Converged intercept:", round(b0, 4))
print("Converged slope:", round(b1, 4))
print("Converged log-likelihood:", round(ll_hat, 4))
print("Slope standard error:", round(se_slope, 3))
print("Wald z:", round(z, 3))
print("Wald z squared:", round(z * z, 3))
print("LR statistic, teaching sample:", round(lr, 3))
# Chi-square critical values are hard-coded because the runtime has no chi-square function.
crit_1df = 3.841
print("LR rejects at 5 percent (1 = yes):", 1 if lr > crit_1df else 0)
print("Wald rejects at 5 percent (1 = yes):", 1 if z * z > crit_1df else 0)

# Step 5: odds ratio and marginal effects.
fit_sum = 0.0
weight_sum = 0.0
for i in range(n):
    p = 1 / (1 + exp(-(b0 + b1 * x[i])))
    fit_sum += p
    weight_sum += p * (1 - p)
print("Sum of fitted probabilities:", round(fit_sum, 4))
print("Odds ratio per turn of leverage:", round(exp(b1), 3))
print("Average marginal effect:", round(b1 * weight_sum / n, 4))
p_bar = 1 / (1 + exp(-(b0 + b1 * xbar)))
print("Marginal effect at mean leverage:", round(b1 * p_bar * (1 - p_bar), 4))

# Step 6: separation. Defaults are now exactly the loans with leverage of 4.0 or more.
y_sep = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
c0 = start0
c1 = 0.0
c1_previous = 0.0
for k in range(10):
    r = newton(c0, c1, y_sep)
    c0 = r[0]
    c1_previous = c1
    c1 = r[1]
r = newton(c0, c1, y_sep)
print("Separated slope after 10 iterations:", round(c1, 3))
print("Separated slope gain in iteration 10:", round(c1 - c1_previous, 2))
print("Separated log-likelihood after 10 iterations:", round(loglik(c0, c1, y_sep), 4))
print("Separated Wald z after 10 iterations:", round(c1 / sqrt(r[4] / r[3]), 4))

# Production model with given coefficients (fitted on 1,000 loans, 80 defaults).
b_const = -3.80
b_lev = 0.55
b_cov = -0.35
b_conc = 0.80
eta_a = b_const + b_lev * 3.0 + b_cov * 4.0 + b_conc
eta_b = eta_a + b_lev
p_a = 1 / (1 + exp(-eta_a))
p_b = 1 / (1 + exp(-eta_b))
print("Borrower A index:", round(eta_a, 4))
print("Borrower B index:", round(eta_b, 4))
print("Borrower A probability:", round(p_a, 4))
print("Borrower B probability:", round(p_b, 4))
print("Odds ratio, leverage:", round(exp(b_lev), 4))
print("Odds ratio, interest cover:", round(exp(b_cov), 4))
print("Odds ratio, concentration:", round(exp(b_conc), 4))
print("Risk ratio, B to A:", round(p_b / p_a, 4))
print("Marginal effect of leverage at A:", round(b_lev * p_a * (1 - p_a), 4))
print("Discrete change, A to B:", round(p_b - p_a, 4))
p_a0 = 1 / (1 + exp(-(eta_a - b_conc)))
print("Concentration effect at A:", round(p_a - p_a0, 4))

# Step 9: likelihood-ratio tests from reported log-likelihoods.
loans = 1000
defaults = 80
rate = defaults / loans
ll0 = loans * (rate * log(rate) + (1 - rate) * log(1 - rate))
ll_full = -241.60
ll_drop = -244.50
print("Events per slope, production model:", round(defaults / 3, 1))
print("Null log-likelihood:", round(ll0, 4))
print("LR statistic, three slopes:", round(2 * (ll_full - ll0), 3))
print("McFadden pseudo-R2:", round(1 - ll_full / ll0, 4))
print("LR statistic, concentration:", round(2 * (ll_full - ll_drop), 3))
# Hard-coded chi-square 5 percent critical values: 7.815 (3 df), 3.841 (1 df); 1 percent: 6.635 (1 df).

# Step 10: cost-based threshold.
cost_fp = 2
cost_fn = 40
p_star = cost_fp / (cost_fp + cost_fn)
print("Cost-based threshold:", round(p_star, 4))
print("Log-odds threshold:", round(log(cost_fp / cost_fn), 4))
print("Expected cost of declining A:", round((1 - p_a) * cost_fp, 4))
print("Expected cost of approving A:", round(p_a * cost_fn, 4))

# Base-rate shift: only the intercept moves when the default rate falls from 8 to 3 percent.
shift = log((0.03 / 0.97) / (0.08 / 0.92))
print("Intercept shift for a 3 percent default rate:", round(shift, 4))
print("Borrower A probability after the shift:", round(1 / (1 + exp(-(eta_a + shift))), 4))""",
            "A second lender fits logit p = −4.20 + 0.60 × leverage − 0.30 × cover + 0.50 × concentrated on 600 loans with 36 defaults, and reports log-likelihoods of −124.00 for the full model and −126.50 with the concentration dummy dropped. For a borrower with leverage 2.5, cover 5.0 and no concentration, (a) find the default probability and the odds; (b) find the probability after one more turn of leverage and compare the change with the marginal effect at the starting point and with the odds ratio; (c) with C_FP = 1 and C_FN = 15, find the threshold and decide; (d) compute the LR statistic for all three slopes, McFadden's R-squared and the LR statistic for the dummy alone, using critical values 7.815 (3 df) and 3.841 (1 df). Then explain why an odds ratio of 1.82 would not raise a borrower at a 50% default probability by 82%.",
            "(a) The index is −4.20 + 0.60 × 2.5 − 0.30 × 5.0 = −4.20, so p = 1/(1 + e^4.2) = 0.0148 and the odds are 0.0150. (b) One more turn gives an index of −3.60 and p = 0.0266, a change of 0.0118. The marginal effect at the start is 0.60 × 0.0148 × 0.9852 = 0.0087, below the actual change because the logistic curve is convex at low p. The odds ratio is e^0.60 = 1.8221; the risk ratio is 0.0266/0.0148 = 1.8003, close to it because p is small. (c) The threshold is 1/(1 + 15) = 0.0625, or ln(1/15) = −2.708 on the log-odds scale. The borrower's 0.0148 is below it, so approve; the expected cost of declining is 0.9852 and of approving is 0.0148 × 15 = 0.2216. At cover 5.0 and no concentration the loan would be flagged only once leverage passed about 4.99 turns. (d) With 36 defaults in 600 loans, ℓ0 = 600 × (0.06 ln 0.06 + 0.94 ln 0.94) = −136.18, so LR = 2 × (−124.00 + 136.18) = 24.36, far above 7.815, and McFadden's R-squared is 1 − 124.00/136.18 = 0.0894. For the dummy alone, LR = 2 × (−124.00 + 126.50) = 5.0, above 3.841, so it is significant at 5%. An odds ratio multiplies the odds, not the probability: a borrower at 0.50 has odds 1.0, which become 1.8221 and a probability of 1.8221/2.8221 = 0.6456, a rise of 0.146 or 29% in relative terms. The 82% reading is nearly right only at the low probabilities where odds and probabilities almost coincide.",
            [
                q('A fitted logit has a coefficient of 0.40 on leverage. Holding the other regressors fixed, one more turn of leverage:', ['raises the default probability by 0.40', 'multiplies the odds of default by e^0.40, about 1.49', 'multiplies the default probability by about 1.49'], 1, 'The coefficient is a change in log-odds, so the odds are multiplied by e^0.40 = 1.49 for every borrower. The probability changes by an amount that depends on p through the factor p(1 − p), and it is not multiplied by 1.49 except approximately when p is very small.'),
                q("A logit with four slopes has a log-likelihood of −120.0, against −150.0 for the intercept-only model. The LR statistic and McFadden's pseudo-R-squared are:", ['LR = 30.0 and pseudo-R-squared = 0.20', 'LR = 60.0 and pseudo-R-squared = 0.25', 'LR = 60.0 and pseudo-R-squared = 0.20'], 2, "LR = 2 × (−120.0 − (−150.0)) = 60.0, to be compared with a chi-square distribution on 4 degrees of freedom. McFadden's R-squared is 1 − (−120.0)/(−150.0) = 1 − 0.80 = 0.20. Forgetting the factor 2 gives 30.0, and dividing the gain by the wrong log-likelihood gives 0.25."),
                q('A fund screens bonds with a logit default model. Wrongly excluding a sound bond costs 1.5 units and holding a bond that defaults costs 30 units. The model gives a bond a default probability of 0.06. The cost-minimising screen:', ['excludes it, because 0.06 exceeds the break-even probability 1.5/31.5 = 0.0476', 'keeps it, because 0.06 is far below the conventional 0.5 cut-off', 'keeps it, because the break-even probability is 30/31.5 = 0.952'], 0, "The break-even probability is C_FP/(C_FP + C_FN) = 1.5/(1.5 + 30) = 0.0476. Excluding costs 0.94 × 1.5 = 1.41 in expectation and holding costs 0.06 × 30 = 1.80, so exclusion is cheaper. The 0.5 cut-off ignores that a missed default costs twenty times a wrong exclusion, and 30/31.5 inverts the ratio. The conclusion also depends on the model's probabilities being well calibrated."),
            ],
        ),
    ),
    (
        '2.24',
        (
            '2.38',
            12,
            'The fundamental law of active management',
            'Relate the information ratio to skill, breadth and the transfer coefficient, correct breadth for correlated bets, and size active risk from a risk-aversion budget.',
            r"""## The analytical question

Lesson 2.24 defined the information ratio as active return per unit of tracking error, and Lesson 2.23 separated factor return from a residual. Both describe what a portfolio did. The forward question is what a manager must be good at, and how the forecasts must be traded, for a given information ratio to be expected, and how much active risk that ratio can carry.

**Skill and the forecasting rule.** Let $\theta_n$ be the residual return of stock $n$ over one forecast horizon, $\omega_n$ its residual risk over that horizon, and $z_n$ a forecast score standardised across stocks to mean 0 and standard deviation 1. The information coefficient is the cross-sectional correlation $\text{IC} = \text{corr}(z_n,\ \theta_n/\omega_n)$. Regressing the risk-scaled return, which has unit variance by construction, on a unit-variance score gives a slope equal to the IC. That is Grinold's forecasting rule:

$$\alpha_n = \text{IC}\cdot\omega_n\cdot z_n$$

Units matter. The IC belongs to a horizon and $\omega_n$ must be the residual risk over that same horizon, so a quarterly IC needs quarterly risk.

**The law.** The manager chooses active weights $h_n$ to maximise $\alpha_P - \lambda\omega_P^2$, where $\alpha_P$ and $\omega_P$ are active return and active risk and $\lambda$ is a risk-aversion coefficient. Write $a_n = \alpha_n/\omega_n = \text{IC}\,z_n$ for risk-scaled alphas and $v_n = h_n\omega_n$ for risk-scaled weights. With uncorrelated residual returns, $\alpha_P = a\cdot v$ and $\omega_P = \lVert v\rVert$, so every portfolio has

$$\text{IR} = \frac{a\cdot v}{\lVert v\rVert} = \lVert a\rVert\cos\vartheta$$

where $\vartheta$ is the angle between the two vectors. The optimum is $v = a/(2\lambda)$, that is $h_n = \alpha_n/(2\lambda\omega_n^2)$, which makes $\cos\vartheta = 1$ and gives $\text{IR} = \lVert a\rVert = \text{IC}\sqrt{\sum z_n^2} \approx \text{IC}\sqrt{N}$. With $T$ independent rebalances a year, annualising the per-period ratio by $\sqrt{T}$ gives Grinold's fundamental law:

$$\text{IR} = \text{IC}\sqrt{\text{BR}}, \qquad \text{BR} = N\,T$$

Breadth BR counts independent bets per year. Skill enters linearly and breadth through a square root, so quadrupling the number of bets is worth only as much as doubling the IC.

**Transfer coefficient.** The cosine above is what Clarke, de Silva and Thorley (2002) call the transfer coefficient TC: the correlation, when both vectors are centred, between risk-scaled weights and risk-scaled forecasts. It is 1 for the unconstrained optimum. A long-only investor cannot underweight a stock by more than its benchmark weight, so negative forecasts on small benchmark names cannot be fully acted on, and turnover and position limits bind too; each pushes TC below 1:

$$\text{IR} = \text{TC}\cdot\text{IC}\cdot\sqrt{\text{BR}}$$

**Correlated bets.** Let the payoff of a bet be its active weight times its residual return, and suppose the $N$ payoffs share a variance $\sigma^2$ and an average pairwise correlation $\rho$. Their sum has variance $N\sigma^2[1 + (N-1)\rho]$ instead of $N\sigma^2$, while the expected total is unchanged, so the information ratio shrinks as if there were only

$$N_{\text{eff}} = \frac{N}{1 + (N-1)\rho}$$

independent bets, a number that can never exceed $1/\rho$ however many stocks are added. Note that $\rho$ is a correlation of payoffs, not of returns: opposite positions in stocks whose returns move together have negatively correlated payoffs. Signals built from overlapping inputs, such as two valuation ratios, overweight the same names and so produce positively correlated payoffs. The same arithmetic applies over time: a slow signal re-traded each quarter recycles one bet instead of creating four.

There is a measurable version. With risk held at its target, each period's active return is proportional to that period's realised IC, so the period's information ratio is the mean IC divided by its standard deviation across periods (Qian and Hua, 2004). Under the assumptions above that standard deviation is $1/\sqrt{N_{\text{eff}}}$, so $\text{IR} = \overline{\text{IC}}/\sigma_{\text{IC}}$ per period, and breadth can be estimated as $1/\sigma_{\text{IC}}^2$ from the series of realised ICs. Any extra variation of the true IC over time, which Qian and Hua call strategy risk, widens $\sigma_{\text{IC}}$ and pulls the ratio below the law.

**Risk budgeting.** Along the efficient set $\alpha_P = \text{IR}\cdot\omega_P$, so the objective is $\text{IR}\,\omega - \lambda\omega^2$, with

$$\omega^{*} = \frac{\text{IR}}{2\lambda}, \qquad U^{*} = \frac{\text{IR}^2}{4\lambda}, \qquad U(\omega) = U^{*} - \lambda(\omega - \omega^{*})^2$$

The last identity prices a mistake: active risk $\omega$ chosen from an inflated ratio costs $\lambda$ times the squared miss from the $\omega^{*}$ that the true ratio would justify.

**What the law assumes.** It needs uncorrelated bets, an IC that is known and the same for every stock and date, a linear score–return relationship, an unconstrained optimiser with a correct risk model, and sizing on residual risk alone. Departures can in principle go either way, since negatively correlated bets would add breadth, but the usual ones lower the ratio: positive payoff correlation, a transfer coefficient below one, and an IC that varies over time or is estimated with error. Read the law as a benchmark under ideal conditions, not as a forecast.

## A worked example

A fictional manager forecasts quarterly residual returns for 500 stocks with IC = 0.04 and rebalances four times a year. The average pairwise correlation of bet payoffs is $\rho = 0.02$, the transfer coefficient is 0.6 and the risk-aversion coefficient is $\lambda = 10$, with returns in decimals.

Step 1, the law as usually quoted. Breadth is $500 \times 4 = 2000$, so $\text{IR} = 0.04\sqrt{2000} = 1.789$.

Step 2, correlated bets. $N_{\text{eff}} = 500/(1 + 499 \times 0.02) = 45.54$ per rebalance, just under the ceiling $1/\rho = 50$. Annual breadth is $4 \times 45.54 = 182.15$ and $\text{IR} = 0.04\sqrt{182.15} = 0.54$. Correlation alone leaves 0.302 of the ideal ratio. Equivalently, the quarterly IC would scatter with standard deviation $1/\sqrt{45.54} = 0.1482$ instead of $1/\sqrt{500} = 0.0447$, so the IC information ratio is $0.04/0.1482 = 0.27$ per quarter, or 0.54 annualised.

Step 3, implementation. $\text{IR} = 0.6 \times 0.54 = 0.324$, which is 0.181 of the figure in Step 1.

Step 4, the forecasting rule for a stock with score $z = 1.5$ and annual residual risk 25%. The IC is quarterly, so the risk must be quarterly: $25\%/\sqrt{4} = 12.5\%$. Then $\alpha = 0.04 \times 12.5\% \times 1.5 = 0.75\%$ for the quarter, which is 3.0% at an annual rate. Feeding the annual 25% to the quarterly IC would give 1.5%, an error of $\sqrt{4}$ that is easy to make.

Step 5, the risk budget. $\omega^{*} = 0.324/(2 \times 10) = 1.62\%$ of active risk, with expected active return $0.324 \times 1.62\% = 0.52\%$ and $U^{*} = 0.324^2/40 = 0.262\%$. Sizing from the Step 1 ratio instead gives $1.789/20 = 8.94\%$. At the true ratio of 0.324 the expected active return at that risk is 2.9%, but the risk penalty is $10 \times 0.0894^2 = 8.0\%$, so value added is −5.1%.

Step 6, can the ratio be verified? With that scatter, one quarter gives IC = 0.04 a $t$-statistic of 0.27, and 20 quarters give $0.27\sqrt{20} = 1.21$. For the portfolio ratio of 0.324, $t = \text{IR}\sqrt{Y}$ reaches 2 only after $(2/0.324)^2 = 38.1$ years. Run backwards, an IR of 0.5 at this IC and TC needs $(0.5/(0.6 \times 0.04))^2 = 434$ independent bets a year, against the 182.15 available.

## Interpretation and failure modes

Every step above removes skill that the headline ratio claimed. Breadth is the usual culprit: counting 500 stocks as 500 independent bets, or four rebalances as four fresh draws, treats overlapping information as new. Estimate $\rho$ from the payoffs themselves.

An IC is an estimate. Selected from many candidate signals it is biased upward (Lesson 2.13), and Step 6 shows that even 20 quarters leave 0.04 only 1.21 standard errors from zero. Realised information ratios over a few years are noisier still, the same power problem as Lesson 2.29. The forecasting rule is also a shrinkage rule: the spread of alphas should be a small fraction of the spread of scores, so treating a score scaled by residual risk as if it were alpha overstates it by a factor of $1/\text{IC}$.

The law is silent about cost. Faster rebalancing raises $T$ only if the IC survives the shorter horizon and the extra turnover does not eat the alpha, and more stocks add breadth only up to $1/\rho$. The transfer coefficient depends on the benchmark, the optimiser and the risk model, so compute it from actual and ideal weights rather than assuming it. And $\lambda$ is the client's preference, not an output of skill: the same ratio supports different risk budgets for different clients, and the formula sizes risk for a ratio without saying whether the ratio is credible.

Finally, the ratio is an expectation of residual performance. If the risk model omits a factor, that factor's return sits inside the residual and part of the apparent skill is an unpriced exposure (Lesson 2.23).

## Implementation

Compute the IC per date and summarise it: `ic = df.groupby("date").apply(lambda g: g["score"].corr(g["fwd_resid"], method="spearman"))`, where `fwd_resid` is the next-period residual from `sm.OLS(r, sm.add_constant(F)).fit().resid`, as in Lesson 2.23. Then `ic.mean()` is the IC, `ic.mean() / ic.std(ddof=1)` is the information ratio of the IC series and `ic.mean() / (ic.std(ddof=1) / np.sqrt(len(ic)))` its t-statistic; `scipy.stats.spearmanr` handles one date at a time. A rank IC resists outliers, but the forecasting rule is linear in $z$, so convert rank scores to z-scores before using it. For breadth, build the matrix of bet payoffs `B = w_active * resid` with dates in rows, take `C = np.corrcoef(B, rowvar=False)`, then `rho = (C.sum() - len(C)) / (len(C) * (len(C) - 1))` and `n_eff = N / (1 + (N - 1) * rho)`; `1 / ic.var(ddof=1)` is a cross-check from the IC series alone. With fewer dates than stocks the matrix is rank-deficient, but its average off-diagonal element is still computable: give it a bootstrap interval over dates (Lesson 2.12), and do not shrink the matrix toward the identity first, because that pulls $\rho$ toward zero and inflates $N_{\text{eff}}$. For the transfer coefficient, take the ideal weights `alpha / (2 * lam * omega**2)`, solve the constrained problem with `scipy.optimize.minimize(..., method="SLSQP", bounds=...)` and a long-only bound, and compute `np.corrcoef(h * omega, alpha / omega)[0, 1]`. Report the IR beside the IC, $N_{\text{eff}}$ and TC, so a reader can see which of the three carries it.""",
            '\\text{IR}=\\text{TC}\\cdot\\text{IC}\\sqrt{N_{\\text{eff}}\\,T},\\qquad N_{\\text{eff}}=\\frac{N}{1+(N-1)\\rho},\\qquad \\omega^{*}=\\frac{\\text{IR}}{2\\lambda}',
            r"""from math import sqrt

# Inputs for the fictional manager.
ic = 0.04            # information coefficient of one quarterly forecast
stocks = 500
rebalances = 4       # independent forecasts per stock per year
rho = 0.02           # average pairwise correlation of bet payoffs
tc = 0.6             # transfer coefficient
z = 1.5              # score of the stock examined in Step 4
resid_risk = 0.25    # its annual residual risk
lam = 10.0           # risk aversion in alpha - lam * risk^2, returns in decimals

# Step 1: the law as usually quoted.
breadth = stocks * rebalances
ir_ideal = ic * sqrt(breadth)
print("Breadth with independent bets:", breadth)
print("IR with independent bets:", round(ir_ideal, 3))

# Step 2: correlated bets.
bets = stocks / (1 + (stocks - 1) * rho)
breadth_eff = bets * rebalances
ir_corr = ic * sqrt(breadth_eff)
print("Effective bets per rebalance:", round(bets, 2))
print("Ceiling on effective bets:", round(1 / rho, 2))
print("Effective breadth per year:", round(breadth_eff, 2))
print("IR with correlated bets:", round(ir_corr, 3))
print("Share of the ideal IR kept after correlation:", round(ir_corr / ir_ideal, 3))
spread_ind = 1 / sqrt(stocks)
spread_corr = 1 / sqrt(bets)
print("IC scatter with independent bets:", round(spread_ind, 4))
print("IC scatter with correlated bets:", round(spread_corr, 4))
print("IC information ratio per quarter:", round(ic / spread_corr, 3))
print("IC information ratio annualised:", round(ic / spread_corr * sqrt(rebalances), 3))

# Step 3: the transfer coefficient.
ir_tc = tc * ir_corr
print("IR with transfer coefficient:", round(ir_tc, 3))
print("Share of the ideal IR kept in total:", round(ir_tc / ir_ideal, 3))

# Step 4: Grinold's forecasting rule needs risk over the same horizon as the IC.
risk_q = resid_risk / sqrt(rebalances)
alpha_q = ic * risk_q * z
print("Quarterly residual risk (percent):", round(risk_q * 100, 2))
print("Alpha per quarter (percent):", round(alpha_q * 100, 3))
print("Alpha at an annual rate (percent):", round(alpha_q * rebalances * 100, 2))
print("Alpha if annual risk meets a quarterly IC (percent):", round(ic * resid_risk * z * 100, 2))

# Step 5: risk budget.
risk_star = ir_tc / (2 * lam)
print("Optimal active risk (percent):", round(risk_star * 100, 2))
print("Expected active return at the optimum (percent):", round(ir_tc * risk_star * 100, 2))
print("Value added at the optimum (percent):", round(ir_tc ** 2 / (4 * lam) * 100, 3))
risk_naive = ir_ideal / (2 * lam)
penalty = lam * risk_naive ** 2
print("Active risk sized from the ideal IR (percent):", round(risk_naive * 100, 2))
print("Expected active return at that risk (percent):", round(ir_tc * risk_naive * 100, 2))
print("Risk penalty at that risk (percent):", round(penalty * 100, 2))
print("Value added at that risk (percent):", round((ir_tc * risk_naive - penalty) * 100, 2))

# Step 6: how well can any of this be verified?
print("IC t-statistic, one quarter:", round(ic / spread_corr, 2))
print("IC t-statistic, 20 quarters:", round(ic / spread_corr * sqrt(20), 2))
print("Years of record for a t-statistic of 2:", round((2 / ir_tc) ** 2, 1))
print("Independent bets needed for an IR of 0.5:", round((0.5 / (tc * ic)) ** 2, 1))""",
            "A second fictional manager has IC 0.03 per monthly forecast, 300 stocks, 12 rebalances a year, an average bet-payoff correlation of 0.03, transfer coefficient 0.5 and λ = 8 with returns in decimals. Compute (a) breadth and the IR as the law is usually quoted; (b) the effective bets per rebalance and the IR with correlated bets; (c) the IR with the transfer coefficient; (d) Grinold's alpha for a stock with z = 2.0 and annual residual risk 30%, for the month and at an annual rate; (e) the optimal active risk and value added, and the value added if risk is sized from the IR in (a); (f) the independent bets a year that an IR of 0.5 would need at this IC and TC. Then say which assumption of the law monthly rebalancing most plausibly breaks.",
            '(a) Breadth is 300 × 12 = 3,600 and IR = 0.03 × √3600 = 1.80. (b) N_eff = 300/(1 + 299 × 0.03) = 300/9.97 = 30.09 per rebalance, just under the ceiling 1/0.03 = 33.3; annual breadth is 12 × 30.09 = 361.08 and IR = 0.03 × √361.08 = 0.570. (c) IR = 0.5 × 0.570 = 0.285. (d) Monthly residual risk is 30%/√12 = 8.66%, so α = 0.03 × 8.66% × 2.0 = 0.52% for the month, which is 6.24% at an annual rate (feeding 30% to a monthly IC would give 1.8%, wrong by √12). (e) ω* = 0.285/(2 × 8) = 1.78% and U* = 0.285²/32 = 0.254%. Sizing from 1.80 gives ω = 1.80/16 = 11.25%, where the expected active return is 0.285 × 11.25% = 3.21% but the risk penalty is 8 × 0.1125² = 10.1%, so value added is −6.92%. (f) (0.5/(0.5 × 0.03))² = 1,111 independent bets a year, about 3.1 times the 361 available. Monthly rebalancing most plausibly breaks independence over time: a persistent signal such as a valuation ratio is re-traded as the same bet, so twelve rebalances are not twelve fresh bets, and a one-month IC may also decay or be eaten by turnover costs, which makes 361 optimistic.',
            [
                q("A manager's IC stays at 0.03 while the number of independent bets a year rises from 400 to 1,600. The information ratio:", ['quadruples', 'doubles', 'rises by about 41%'], 1, 'IR = IC × √BR. At 400 bets it is 0.03 × 20 = 0.60 and at 1,600 bets it is 0.03 × 40 = 1.20, so it doubles. Breadth enters through a square root, which is why a fourfold increase in bets only doubles the ratio.'),
                q('A manager has IC 0.05, 100 stocks traded once a year, bet payoffs with average pairwise correlation 0.04 and a transfer coefficient of 0.8. The expected information ratio is closest to:', ['0.18', '0.40', '0.50'], 0, 'N_eff = 100/(1 + 99 × 0.04) = 100/4.96 = 20.16 independent bets, so IR = 0.8 × 0.05 × √20.16 = 0.04 × 4.49 = 0.18. The figure 0.50 is 0.05 × √100, ignoring both frictions, and 0.40 applies the transfer coefficient but not the correlation.'),
                q('A pitch quotes IR 1.0 for a mandate whose realistic IR is 0.40. With value added U = α − λω² and λ = 5 (returns in decimals), sizing active risk from the pitch instead of the realistic ratio gives value added of:', ['+0.8%, the same as at the optimum', '+4.0%, because the extra risk earns extra return', '−1.0%, which is 1.8 points below the optimum'], 2, 'The optimal risk is 0.40/10 = 4% with U* = 0.40²/20 = 0.8%. The pitch implies 1.0/10 = 10%, where the expected active return is 0.40 × 10% = 4.0% but the penalty is 5 × 0.10² = 5.0%, so U = −1.0%. The shortfall is λ(ω − ω*)² = 5 × 0.06² = 1.8%.'),
            ],
        ),
    ),
    (
        '2.38',
        (
            '2.39',
            12,
            'Combining views with equilibrium: Black–Litterman',
            'Blend market-implied equilibrium returns with explicit, confidence-weighted views, and trace how the posterior returns and the optimal weights respond.',
            r"""## The analytical question

Lesson 2.24 measured the risk of a portfolio whose weights were already chosen. This lesson takes up the earlier decision: which weights to hold when you hold opinions about returns. Lesson 2.3 showed how slowly the standard error of a mean falls as data accumulate, and Lesson 2.10 warned that a covariance matrix estimated from few observations cannot safely be inverted for portfolio optimization. Here the warning becomes arithmetic, and a widely used repair, the model of Black and Litterman (1992), is built from three ingredients: returns implied by the market, a statement of how uncertain those returns are, and views that carry their own stated confidence.

**Why error is amplified.** With risk-aversion coefficient $\delta$, an unconstrained investor who maximizes $w'\mu - \tfrac{\delta}{2}w'\Sigma w$, where $\mu$ holds expected excess returns, chooses

$$w^{*} = (\delta\Sigma)^{-1}\mu$$

The weights are a linear map of the mean vector, and the map is $\Sigma^{-1}/\delta$. An error $\varepsilon$ in the means therefore changes the weights by $(\delta\Sigma)^{-1}\varepsilon$. Assets that resemble each other make $\Sigma$ nearly singular, so its inverse has a very large eigenvalue, and the optimizer reads a small difference between similar assets as a large, confident trade. Best and Grauer (1991) documented this sensitivity, and Michaud (1989) called the outcome error maximization.

Take the covariance matrix used in the example below and $\delta = 2.5$. Its inverse has entries 28.125, −12.5 and 50. A one-point error in asset A's mean moves the weights by 11.25 points in A and −5 points in B. Sampling error is far larger than one point: ten years of annual returns with 20% volatility give a standard error of 6.3 points on the mean, and a single such error in asset A moves the weights by about +71 and −32 points. A historical mean is too imprecise to feed through $\Sigma^{-1}$.

**Reverse optimization.** Instead of estimating $\mu$, ask which $\mu$ would make the market portfolio optimal. Solving $w_{mkt} = (\delta\Sigma)^{-1}\pi$ for $\pi$ gives

$$\pi = \delta\,\Sigma\,w_{mkt}$$

These equilibrium returns are consistent with $\Sigma$ by construction, so an investor with no views who optimizes with $\pi$ holds the market portfolio. The market also pins down the risk aversion: multiplying by $w_{mkt}'$ gives $\delta = \tfrac{w_{mkt}'\pi}{w_{mkt}'\Sigma w_{mkt}}$, the market's expected excess return per unit of its variance.

**The role of $\tau$.** The vector $\pi$ is a reference point, not a certainty. The model treats the true mean vector as uncertain around it, $\mu \sim N(\pi, \tau\Sigma)$. A sample mean of $T$ independent observations has covariance $\Sigma/T$, so $\tau$ plays the part of $1/T$: a small value says the mean is much better known than a single return. It is a modeling choice, not an estimate. It leaves $\pi$ unchanged and sets only how easily a view can move the posterior away from $\pi$.

**Views.** A set of $k$ views is written $P\mu = Q + \eta$ with $\eta \sim N(0,\Omega)$. $P$ is a $k \times n$ pick matrix, $Q$ holds the view returns, and $\Omega$, usually diagonal, holds the variances of the view errors. An absolute view, "A returns 8%", has row $(1, 0)$ and $Q = 0.08$. A relative view, "A beats B by 3 points", has row $(1, -1)$ and $Q = 0.03$. A row such as $(1, -\tfrac12, -\tfrac12)$ compares one asset with the average of two. A diagonal entry of $\Omega$ is a squared margin of error: "plus or minus 2 points" means $0.02^2 = 0.0004$. A view states an expected return with an uncertainty. It is not a prediction of what will happen.

**The posterior.** The prior and the views are two independent noisy measurements of $\mu$. Weighting each by its precision, the inverse of its covariance, gives the posterior mean

$$E[R] = \left[(\tau\Sigma)^{-1} + P'\Omega^{-1}P\right]^{-1}\left[(\tau\Sigma)^{-1}\pi + P'\Omega^{-1}Q\right]$$

This is Lesson 2.9's Bayes update for normal distributions, and also the mixed-estimation estimator of Theil and Goldberger (1961). The Woodbury identity gives an equivalent form that inverts only a $k \times k$ matrix:

$$E[R] = \pi + \tau\Sigma P'\left(\tau P\Sigma P' + \Omega\right)^{-1}\left(Q - P\pi\right)$$

Read it as: start at equilibrium, then move by a gain times the disagreement $Q - P\pi$. If $\Omega \to \infty$ the view is ignored and $E[R] = \pi$. If $\Omega \to 0$ the view is imposed exactly, $P\,E[R] = Q$.

**Optimal weights.** The investor optimizes again with the posterior, $w^{*} = (\delta\Sigma)^{-1}E[R]$. Substituting the second form of $E[R]$ and cancelling $\Sigma$ gives

$$w^{*} = w_{mkt} + \frac{\tau}{\delta}\,P'\left(\tau P\Sigma P' + \Omega\right)^{-1}\left(Q - P\pi\right)$$

Two facts follow. First, the whole tilt lies along the rows of $P$, so an asset that appears in no view keeps its market weight, and errors cannot leak into it through $\Sigma^{-1}$. Second, for a single view the tilt is proportional to the disagreement divided by the sum of the view portfolio's prior variance and the view's own variance. That ratio never exceeds the disagreement divided by $\Omega$, which caps the tilt for any finite margin of error, and confidence saturates as $\Omega \to 0$. Factoring $\tau$ out of the inverse shows that the posterior mean and the weights depend on $\tau$ and $\Omega$ only through the ratio $\Omega/\tau$, so for those two outputs choosing $\tau$ and choosing $\Omega$ are one decision. The posterior uncertainty $M^{-1}$ defined below still scales with $\tau$ itself.

## A worked example

Two fictional funds, A (cyclical) and B (defensive), have annual excess-return covariance matrix

$$\Sigma = \begin{pmatrix} 0.0400 & 0.0100 \\ 0.0100 & 0.0225 \end{pmatrix}$$

Volatilities are 20% and 15%, and the correlation is 1/3. Market weights are 60% and 40%, $\delta = 2.5$ and $\tau = 0.05$.

Step 1, reverse optimization. $\Sigma w_{mkt} = (0.04 \times 0.6 + 0.01 \times 0.4,\; 0.01 \times 0.6 + 0.0225 \times 0.4) = (0.028, 0.015)$, so

$$\pi = 2.5 \times (0.028, 0.015) = (0.0700, 0.0375)$$

Check: the market's expected excess return is $0.6 \times 0.07 + 0.4 \times 0.0375 = 0.0570$, its variance is $0.6 \times 0.028 + 0.4 \times 0.015 = 0.0228$, and the ratio is 2.5.

Step 2, the view. The analyst expects A to beat B by 5 points a year, give or take 2 points: $P = (1, -1)$, $Q = 0.05$ and $\Omega = 0.02^2 = 0.0004$. Equilibrium already implies $P\pi = 0.0700 - 0.0375 = 0.0325$, so the view is 1.75 points more bullish on A than the market. The view portfolio's prior variance is $\tau P\Sigma P' = 0.05 \times (0.04 + 0.0225 - 0.02) = 0.002125$, a standard deviation of 4.6 points, looser than the view's 2.

Step 3, the posterior mean from the matrix formula. The matrix $\tau\Sigma$ has entries 0.002, 0.0005 and 0.001125, and determinant $0.002 \times 0.001125 - 0.0005^2 = 2.0 \times 10^{-6}$. Swapping the diagonal, negating the off-diagonal and dividing by the determinant gives

$$(\tau\Sigma)^{-1} = \begin{pmatrix} 562.5 & -250 \\ -250 & 1000 \end{pmatrix}$$

The view adds $P'\Omega^{-1}P$, so the posterior precision $M$ and its determinant are

$$P'\Omega^{-1}P = 2500\begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}, \qquad M = \begin{pmatrix} 3062.5 & -2750 \\ -2750 & 3500 \end{pmatrix}$$

$$\det M = 3062.5 \times 3500 - 2750^2 = 3{,}156{,}250$$

The right-hand side is $(\tau\Sigma)^{-1}\pi = (30, 20)$ plus $P'\Omega^{-1}Q = 125\,(1, -1)$, which totals $(155, -105)$. The first part equals $(\delta/\tau)\,w_{mkt}$, a useful check. Then

$$E[R] = \frac{1}{3{,}156{,}250}\begin{pmatrix} 3500 & 2750 \\ 2750 & 3062.5 \end{pmatrix}\begin{pmatrix} 155 \\ -105 \end{pmatrix} = \frac{1}{3{,}156{,}250}\begin{pmatrix} 253{,}750 \\ 104{,}687.5 \end{pmatrix} = (0.0804,\; 0.0332)$$

A's expected return rises from 7.00% to 8.04% and B's falls from 3.75% to 3.32%. The posterior spread is 4.72 points, between the equilibrium 3.25 and the view 5.00. It sits 84% of the way to the view because the view's precision, 2,500, dwarfs the prior's 470.6. The update form agrees: $\Sigma P' = (0.03, -0.0125)$ and the scalar $0.0175 / (0.0425 + 0.008) = 0.3465$ multiplies it, shifting the means by $+0.0104$ and $-0.0043$.

Step 4, the weights. With $\Sigma^{-1}$ entries 28.125, −12.5 and 50, $w^{*} = (\delta\Sigma)^{-1}E[R] = (0.7386,\; 0.2614)$. The 60/40 market portfolio becomes about 73.9/26.1. The tilt formula gives the same answer: $\tfrac{0.05}{2.5} \times \tfrac{0.0175}{0.002125 + 0.0004} = 0.1386$ moves from B to A.

Step 5, lower $\Omega$ moves the weights further, with diminishing returns:

- $\Omega = 0.0025$ (plus or minus 5 points): posterior spread 4.05 points, weights 67.6/32.4.
- $\Omega = 0.0004$ (plus or minus 2 points): spread 4.72, weights 73.9/26.1.
- $\Omega = 0.0001$ (plus or minus 1 point): spread 4.92, weights 75.7/24.3.
- $\Omega \to 0$: spread 5.00, weights 76.5/23.5. The tilt is $(Q - P\pi)/(\delta\,P\Sigma P') = 0.0175 / (2.5 \times 0.0425) = 0.1647$.

Cutting the margin of error from 5 points to 2 adds 6.3 points of weight, cutting it from 2 to 1 adds only 1.9, and no confidence can add more than the ceiling of 16.5.

## Interpretation and failure modes

- **Where $\Omega$ comes from.** Nothing in the model supplies it. A common default, from He and Litterman (1999), sets each diagonal entry equal to the prior variance of its view portfolio, $\tau P\Sigma P'$, which gives prior and view equal weight: here $\Omega = 0.002125$ puts the posterior spread at the midpoint, 4.125 points, and the weights at 68.2/31.8. Idzorek (2005) instead converts a stated percentage confidence into $\Omega$. Either way the margin of error should be earned from the analyst's recorded forecast errors; Lesson 2.29 shows how little a short record establishes.
- **The prior can be wrong.** $\pi$ inherits the market weights and $\delta$. A stale or mismeasured benchmark gives a prior that is consistent only with itself. The model repairs the mean inputs, not the covariance matrix: $\Sigma$ is still estimated with error, and shrinkage, which the econometrics course treats in Lesson 3.22, is the usual remedy.
- **Where the amplification went.** A view on the spread of two near-identical assets has a tiny $P\Sigma P'$, so the full-confidence ceiling $(Q - P\pi)/(\delta\,P\Sigma P')$ is enormous, and a small $\Omega$ brings back the extreme long/short pair warned of above. The model confines error to the directions you name and to the margin of error you assert. It does not make a near-singular $\Sigma$ harmless.
- **Unconstrained means unconstrained.** Relative views keep the weights summing to one, but absolute views do not (see the assignment), and shorts are allowed. With mandate constraints the closed form no longer holds, and the posterior inputs go to a numerical optimizer. Posterior uncertainty about the means is $M^{-1}$, smaller than $\tau\Sigma$: A's mean variance falls from 0.00200 to 0.00111. Some implementations add $M^{-1}$ to $\Sigma$ before optimizing, so that the return covariance reflects the uncertainty that remains about the means.
- **Views interact.** Rows of $P$ that overlap, contradict each other or restate the same evidence count that evidence twice, and a diagonal $\Omega$ assumes independent errors. Inspect the implied view returns $P\,E[R]$ to see how far each view was pulled from its $Q$.
- **A neutral anchor is not a forecast.** If you do not accept the market portfolio as optimal for a representative investor, $\pi$ is only a reference point. The model combines assumptions consistently; it validates none of them, and nothing here recommends holding any portfolio.
- **Timing.** A view formed with information that was not yet public leaks hindsight, as Lesson 2.27 describes. Log each view's date, $Q$ and $\Omega$ before the outcome is known.

## Implementation

In NumPy, build $P$ as a $k \times n$ array and $\Omega$ as a $k \times k$ array. Use `numpy.linalg.inv` only for small illustrations. For real work solve the systems with `numpy.linalg.solve` or `scipy.linalg.solve(M, rhs, assume_a="pos")`, and prefer the update form when $k$ is much smaller than $n$. Estimate $\Sigma$ with a shrinkage estimator such as `sklearn.covariance.LedoitWolf`, and check `numpy.linalg.cond(Sigma)`: a large condition number is the amplification described above. Verify that the two forms of $E[R]$ agree with `numpy.allclose`, and that setting $Q = P\pi$ returns the market weights. The third-party package PyPortfolioOpt implements the model as `pypfopt.black_litterman.BlackLittermanModel`. For constrained weights, pass the posterior mean and covariance to `scipy.optimize.minimize` with the SLSQP method or to a convex solver. A report should show the weights under at least three values of $\Omega$, as in Step 5, and one change of $\pm 1$ point in each $Q$.""",
            '\\pi=\\delta\\Sigma w_{\\text{mkt}},\\qquad E[R]=\\left[(\\tau\\Sigma)^{-1}+P^{\\top}\\Omega^{-1}P\\right]^{-1}\\left[(\\tau\\Sigma)^{-1}\\pi+P^{\\top}\\Omega^{-1}Q\\right]',
            r"""from math import sqrt

# Fictional two-asset market. Every return is an annual excess return.
sAA = 0.04
sAB = 0.01
sBB = 0.0225
wA = 0.6
wB = 0.4
delta = 2.5
tau = 0.05

# Step 0: how an input error moves unconstrained weights, w = inverse(Sigma) mu / delta.
detS = sAA * sBB - sAB * sAB
iAA = sBB / detS
iAB = -sAB / detS
iBB = sAA / detS
print("Inverse covariance AA:", round(iAA, 3))
print("Inverse covariance AB:", round(iAB, 3))
print("Inverse covariance BB:", round(iBB, 3))
print("Weight shift A per point of error:", round(iAA * 0.01 / delta, 4))
print("Weight shift B per point of error:", round(iAB * 0.01 / delta, 4))
se = 0.20 / sqrt(10)
print("Standard error of a ten-year mean:", round(se, 4))
print("Weight shift A per standard error:", round(iAA * se / delta, 4))
print("Weight shift B per standard error:", round(iAB * se / delta, 4))

# Step 1: reverse optimization, pi = delta * Sigma * market weights.
piA = delta * (sAA * wA + sAB * wB)
piB = delta * (sAB * wA + sBB * wB)
print("Prior return A:", round(piA, 4))
print("Prior return B:", round(piB, 4))
premium = wA * piA + wB * piB
variance = wA * (sAA * wA + sAB * wB) + wB * (sAB * wA + sBB * wB)
print("Market premium:", round(premium, 4))
print("Market variance:", round(variance, 4))
print("Implied risk aversion:", round(premium / variance, 3))

# Step 2: one relative view, A minus B, so P = [1, -1].
q = 0.05
omega = 0.0004
priorView = piA - piB
viewVar = tau * (sAA + sBB - 2 * sAB)
print("Prior view return:", round(priorView, 4))
print("Prior view variance:", round(viewVar, 6))
print("Precision weight on the view:", round((1 / omega) / (1 / omega + 1 / viewVar), 4))

# Step 3: posterior mean by the matrix formula, using the 2 x 2 inverse by hand.
def blend(qv, om):
    a = tau * sAA
    b = tau * sAB
    d = tau * sBB
    det = a * d - b * b
    p11 = d / det
    p12 = -b / det
    p22 = a / det
    m11 = p11 + 1 / om
    m12 = p12 - 1 / om
    m22 = p22 + 1 / om
    r1 = p11 * piA + p12 * piB + qv / om
    r2 = p12 * piA + p22 * piB - qv / om
    detm = m11 * m22 - m12 * m12
    eA = (m22 * r1 - m12 * r2) / detm
    eB = (-m12 * r1 + m11 * r2) / detm
    nA = (sBB * eA - sAB * eB) / (delta * detS)
    nB = (-sAB * eA + sAA * eB) / (delta * detS)
    return [p11, p12, p22, m11, m12, m22, r1, r2, detm, eA, eB, nA, nB]

s = blend(q, omega)
print("Prior precision AA:", round(s[0], 1))
print("Prior precision AB:", round(s[1], 1))
print("Prior precision BB:", round(s[2], 1))
print("Posterior precision AA:", round(s[3], 1))
print("Posterior precision AB:", round(s[4], 1))
print("Posterior precision BB:", round(s[5], 1))
print("Right-hand side A:", round(s[6], 1))
print("Right-hand side B:", round(s[7], 1))
print("Determinant of posterior precision:", round(s[8], 0))
print("Posterior return A:", round(s[9], 4))
print("Posterior return B:", round(s[10], 4))
print("Posterior view return:", round(s[9] - s[10], 4))

# Cross-check with the update form: pi + tau Sigma P' (tau P Sigma P' + omega)^-1 (q - P pi).
gain = (q - priorView) / ((sAA + sBB - 2 * sAB) + omega / tau)
print("Update form shift A:", round((sAA - sAB) * gain, 4))
print("Update form shift B:", round((sAB - sBB) * gain, 4))

# Step 4: optimal weights, (delta Sigma)^-1 E[R].
print("Weight A:", round(s[11], 4))
print("Weight B:", round(s[12], 4))
print("Posterior variance of mean A:", round(s[5] / s[8], 5))

# Step 5: a lower omega moves the weights further, up to a ceiling.
low = blend(q, 0.0025)
print("Low confidence view return:", round(low[9] - low[10], 4))
print("Low confidence weight A:", round(low[11], 4))
print("Low confidence weight B:", round(low[12], 4))
high = blend(q, 0.0001)
print("High confidence view return:", round(high[9] - high[10], 4))
print("High confidence weight A:", round(high[11], 4))
print("High confidence weight B:", round(high[12], 4))
tilt = (q - priorView) / (delta * (sAA + sBB - 2 * sAB))
print("Full confidence weight A:", round(wA + tilt, 4))
print("Full confidence weight B:", round(wB - tilt, 4))
mid = blend(q, viewVar)
print("Default omega view return:", round(mid[9] - mid[10], 5))
print("Default omega weight A:", round(mid[11], 4))
print("Default omega weight B:", round(mid[12], 4))""",
            'Keep the covariance matrix, the 60/40 market weights, risk aversion 2.5 and τ = 0.05, but replace the relative view with an absolute view that fund B returns 6% a year, give or take 1.5 points (Ω = 0.000225). Compute the posterior expected returns and the optimal weights. Then explain why the weight on A does not move although its expected return does, and what the total weight means.',
            "The view is P = (0, 1), Q = 0.06 and Pπ = 0.0375, so the disagreement is 0.0225. The view portfolio's prior variance is τ times the variance of B, 0.05 × 0.0225 = 0.001125, so the view carries precision weight 0.001125 / (0.001125 + 0.000225) = 0.8333, and B's posterior mean is 0.0375 + 0.8333 × 0.0225 = 0.05625. ΣP′ = (0.01, 0.0225), so A's mean shifts by (0.01 / 0.0225) × 0.01875 = 0.00833, to 0.07833. For the weights, w* = w_mkt + (τ/δ) P′ (τPΣP′ + Ω)⁻¹ (Q − Pπ): the scalar is 0.02 × 0.0225 / 0.00135 = 0.3333, so w* = (0.6, 0.7333). A's expected return rises only because A is positively correlated with B, and the optimizer already prices that correlation, so the tilt lies along P′ = (0, 1) and the weight on A stays at 0.6. The weights total 1.3333: the extra 0.3333 is financed by borrowing at the risk-free rate, because the unconstrained solution has no budget constraint. A fully invested long-only mandate needs explicit constraints, and then the closed form no longer applies.",
            [
                q('A single relative view has equilibrium value Pπ = 0.015 and Q = 0.045. The prior variance of the view portfolio, τPΣP′, is 0.0012 and the analyst sets the view variance Ω to 0.0004. What is the posterior expected value of the view portfolio?', ['0.0300, the midpoint of 0.015 and 0.045', '0.0375', '0.0450, because the view overrides equilibrium'], 1, "The view's precision weight is the prior variance over the sum of variances: 0.0012 / (0.0012 + 0.0004) = 0.75. The posterior is 0.015 + 0.75 × (0.045 − 0.015) = 0.0375. The midpoint 0.0300 would need Ω = 0.0012, and 0.0450 would need Ω = 0."),
                q('Two assets have variances 0.04 and 0.09 and covariance 0.012. Market weights are 0.7 and 0.3 and the risk-aversion coefficient is 3. What equilibrium excess return does reverse optimization assign to the second asset?', ['0.1062', '0.0810', '0.0948'], 0, "π = δΣw. For the second asset, π₂ = 3 × (0.012 × 0.7 + 0.09 × 0.3) = 3 × (0.0084 + 0.0270) = 0.1062. The figure 0.0810 drops the covariance term (3 × 0.09 × 0.3), and 0.0948 is the first asset's equilibrium return."),
                q('A three-asset market has weights (0.5, 0.3, 0.2). The only view is a relative view that asset 1 outperforms asset 2, with P = (1, −1, 0) and Q above Pπ. Using w* = (δΣ)⁻¹E[R] with the same Σ that generated π, what is the posterior weight on asset 3?', ['Above 0.2, because asset 3 is correlated with the assets in the view', 'Below 0.2, because capital moves toward asset 1', 'Exactly 0.2, because the weight change lies along (1, −1, 0)'], 2, 'Substituting the update form of E[R] gives w* − w_mkt = (τ/δ) P′ (τPΣP′ + Ω)⁻¹ (Q − Pπ), a multiple of P′ = (1, −1, 0). The third component of that change is zero, so asset 3 keeps 0.2. Its expected return does change through the covariances, but the optimizer already accounts for that correlation.'),
            ],
        ),
    ),
    (
        '2.26',
        (
            '2.40',
            13,
            'Backtesting value at risk: exceedances, Kupiec and Christoffersen tests',
            "Test whether a value-at-risk model's exceedances have the right frequency and no memory, and judge how much a passed or failed backtest really establishes.",
            r"""## The analytical question

Lesson 2.25 defined value at risk and expected shortfall and named the Kupiec test as the check on exceedance counts. This lesson builds that test and Christoffersen's companion from the likelihood, adds the regulatory zone rule, and asks what a passed or failed backtest can establish.

**The hit sequence.** Let $L_t$ be the loss on day $t$, positive when money is lost as in Lesson 2.25, and let $\text{VaR}_t$ be the loss threshold forecast at the end of day $t-1$ so that it is exceeded with probability $p$. For a 99% VaR, $p = 0.01$. The hit indicator is

$$I_t = \mathbf{1}\{L_t > \text{VaR}_t\}$$

A model has correct conditional coverage when $P(I_t = 1 \mid \text{information at } t-1) = p$ on every day, which is the same as saying the hits are independent Bernoulli($p$) draws (Christoffersen, 1998). That statement has two testable parts: the hit rate is right, and hits carry no memory. Two bookkeeping rules come first. The forecast must use only information available at $t-1$, and the loss must come from the same positions the VaR describes; otherwise the hits measure the process rather than the model. The backtest should also use one-day forecasts, because ten-day losses measured every day overlap and make the hits dependent by construction.

**Counting exceedances.** If the model is right, the number of hits in $T$ days is binomial, $x \sim \text{Binomial}(T, p)$, with mean $Tp$ and variance $Tp(1-p)$. Kupiec (1995) turned this into a likelihood-ratio test of $H_0: \pi = p$, where $\pi$ is the true hit probability. The maximum-likelihood estimate is $\hat\pi = x/T$, and

$$LR_{pof} = -2\ln\!\left[(1-p)^{T-x}p^{x}\right] + 2\ln\!\left[\left(1-\tfrac{x}{T}\right)^{T-x}\left(\tfrac{x}{T}\right)^{x}\right]$$

is asymptotically $\chi^2_1$, with a 5% critical value of 3.841. This proportion-of-failures test is two-sided, so too few hits reject as well as too many. When $x = 0$ the term $0\ln 0$ is taken as zero.

**Independence.** Count transitions between consecutive days: $n_{ij}$ is the number of days $t$ with $I_{t-1}=i$ and $I_t=j$, a $2\times 2$ table that sums to $T-1$. Christoffersen's alternative is a first-order Markov chain with $\pi_{01} = P(I_t=1 \mid I_{t-1}=0)$ and $\pi_{11} = P(I_t=1 \mid I_{t-1}=1)$, estimated by $\hat\pi_{01} = n_{01}/(n_{00}+n_{01})$ and $\hat\pi_{11} = n_{11}/(n_{10}+n_{11})$. Under independence both equal one probability, estimated by $\hat\pi = (n_{01}+n_{11})/(T-1)$:

$$LR_{ind} = -2\ln\!\left[(1-\hat\pi)^{n_{00}+n_{10}}\hat\pi^{\,n_{01}+n_{11}}\right] + 2\ln\!\left[(1-\hat\pi_{01})^{n_{00}}\hat\pi_{01}^{\,n_{01}}(1-\hat\pi_{11})^{n_{10}}\hat\pi_{11}^{\,n_{11}}\right]$$

This is also asymptotically $\chi^2_1$. It ignores the level of the hit rate and compares only the chance of a hit after a calm day with the chance after a hit day.

**Conditional coverage.** Adding the two statistics tests both parts at once:

$$LR_{cc} = LR_{pof} + LR_{ind} \sim \chi^2_2$$

The 5% critical value is 5.991. The identity is exact when the coverage statistic uses the same $T-1$ observations as the transition table, because the derivation conditions on the first day. Using all $T$ days, the usual practice, changes the statistic only slightly at $T = 250$.

**The Basel traffic light.** The Basel Committee (1996) counts exceptions of a one-day 99% VaR over the latest 250 trading days. Zero to four is the green zone, five to nine the yellow zone and ten or more the red zone, and the capital multiplier rises through the yellow zone to its largest increment in the red. The cut points come from the same binomial distribution: a correct model lands in the green zone with probability 0.892, in the yellow with 0.108 and in the red with 0.00025. The rule looks at the count only, and only at too many.

## A worked example

A fictional desk reports a one-day 99% VaR on each of 250 trading days, and 7 days exceed it.

Step 1, the count. Under a correct model, $x \sim \text{Binomial}(250, 0.01)$ has mean 2.5 and standard deviation 1.57. The exact probability of 7 or more exceedances is 0.0137, and 7 falls in the yellow zone.

Step 2, Kupiec. With $\hat\pi = 7/250 = 0.028$, the log-likelihood is $-34.6784$ at $\pi = 0.01$ and $-31.9299$ at $\hat\pi$, so $LR_{pof} = 2 \times 2.7485 = 5.497$. That exceeds 3.841, so the hit rate is rejected at 5%.

Step 3, the transitions. The seven hits arrive as a run of three days, a run of two days and two isolated days, none on the first or last day. The 249 consecutive pairs of days give $n_{00} = 238$, $n_{01} = 4$, $n_{10} = 4$ and $n_{11} = 3$. After a calm day the hit chance is $\hat\pi_{01} = 4/242 = 0.0165$, after a hit day it is $\hat\pi_{11} = 3/7 = 0.4286$, and pooled it is $\hat\pi = 7/249 = 0.0281$. The log-likelihood is $-31.9015$ under independence and $-25.1577$ under the Markov alternative, so $LR_{ind} = 2 \times 6.7438 = 13.488$, far above 3.841.

Step 4, conditional coverage. $LR_{cc} = 5.497 + 13.488 = 18.985$, far above 5.991, so the model is rejected on both counts: the hit rate is too high and the hits are clustered.

Step 5, the same count without clustering. Suppose the seven hits are all isolated, so $n_{00} = 235$, $n_{01} = 7$, $n_{10} = 7$ and $n_{11} = 0$. Then $LR_{pof}$ is unchanged at 5.497, but $LR_{ind} = 0.405$ and $LR_{cc} = 5.902$, just under 5.991. Kupiec's test rejects and the conditional-coverage test does not: when only one component is wrong, the second degree of freedom spent on the clean one costs power. The traffic light calls both desks yellow.

Step 6, power. With a correct model and $T = 250$, the nominal 5% Kupiec test rejects it with probability 0.0948. Zero exceedances has probability 0.0811 and gives $LR_{pof} = 5.025$, so the test also rejects a correct model for having no hits. If the true hit rate is 2%, double the stated 1%, the test rejects with probability only 0.2427 in 250 days, and a desk with that true rate still lands in the green zone with probability 0.4387. With 1,250 days (five years) the rejection probability rises to 0.8689.

## Interpretation and failure modes

- **Read the pair of statistics.** The failing test says what is wrong. A failed $LR_{pof}$ with a clean $LR_{ind}$ points to the level: too many hits mean a volatility estimate that is too low or tails thinner than the data's, and too few mean a model that is too conservative. A clean $LR_{pof}$ with a failed $LR_{ind}$ means the average is right but the model reacts too slowly to changing risk, so hits arrive in clusters. The EWMA and GARCH(1,1) updates of Lesson 2.18 are the usual remedies.
- **Low power.** With 2.5 expected hits the test has little to work with, so a non-rejection is weak evidence for the model (Lesson 2.29). The traffic light errs in both directions: a correct model leaves the green zone with probability about 0.108, while a model whose true hit rate is double the stated one stays green with probability 0.4387. More power comes from a longer sample or a less extreme level: at 95% the same 250 days hold 12.5 expected hits, though they say less about the far tail. State the power against a named alternative beside every pass.
- **Asymptotics at small counts.** The chi-square approximation is poor when expected counts are tiny, as Step 6 shows. Use the exact binomial test, or simulate the statistic under independent Bernoulli($p$) hits. In the transition table, a handful of hits means $n_{11}$ is a handful of days at most, so the statistic can hinge on one adjacent pair.
- **First-order dependence only.** The Markov alternative sees only dependence between consecutive days. Christoffersen and Pelletier (2004) test the durations between hits, and Engle and Manganelli (2004) regress hits on their own lags and on the VaR forecast, which can find dependence at other lags.
- **Estimation risk and multiplicity.** If VaR parameters are estimated in a rolling window, the standard null distributions are distorted (Escanciano and Olmo, 2010). Testing many desks, levels and windows flags some correct models by chance (Lesson 2.13), and recalibrating after seeing the hits turns the backtest into in-sample fitting (Lesson 2.27).
- **Expected shortfall.** Hits count how often a VaR is exceeded, not by how much, so they cannot validate expected shortfall. Gneiting (2011) showed that expected shortfall alone has no consistent scoring function, that is, it is not elicitable. Fissler and Ziegel (2016) showed that the pair of VaR and expected shortfall is jointly elicitable, and Acerbi and Székely (2014) proposed tests that rely on simulation. There is no agreed counterpart to Kupiec and Christoffersen for expected shortfall, so it remains an open problem, and the Basel market-risk framework that adopted expected shortfall for capital still tests models through VaR exceptions.

## Implementation

Build the hit series with each forecast aligned to the day it describes. In pandas, shift a rolling-window forecast with `.shift(1)` so that it uses data through the previous day, then take `hits = (loss > var_forecast).astype(int).to_numpy()`. Converting to an array matters: slices of a pandas Series align on the index rather than on position, which would compare each day with itself. Take `x = hits.sum()` and `T = len(hits)`, count the four transition types with boolean comparisons of `hits[:-1]` and `hits[1:]`, and compute log-likelihoods with `scipy.special.xlogy`, which applies the $0\ln 0 = 0$ convention. Get p-values from `scipy.stats.chi2.sf(lr, df)`, and the critical values 3.841 and 5.991 from `scipy.stats.chi2.ppf(0.95, 1)` and `chi2.ppf(0.95, 2)`. The null distribution of the count is `scipy.stats.binom`, and `scipy.stats.binomtest(x, T, p)` gives the exact test. For finite-sample critical values, simulate several thousand Bernoulli($p$) sequences with `numpy.random.default_rng`, compute the statistic on each and take its 95th percentile. A report should give $T$, $x$, the expected count, the three statistics with their degrees of freedom and p-values, the Basel zone, and the power against a stated alternative.""",
            'LR_{cc}=LR_{pof}+LR_{ind}\\sim\\chi^{2}_{2},\\qquad LR_{pof}=2\\ln\\frac{(x/T)^{x}(1-x/T)^{T-x}}{p^{x}(1-p)^{T-x}}',
            r"""from math import exp, floor, log, sqrt

# Chi-square 5% critical values are hard-coded because the guided runtime has no
# chi-square function: 3.841 for one degree of freedom and 5.991 for two.
CRIT1 = 3.841
CRIT2 = 5.991

# Fictional desk: a one-day 99% VaR over 250 trading days with 7 exceedances.
t = 250
p0 = 0.01
x = 7

def xlogy(c, v):
    # c * ln(v) with the convention 0 * ln(0) = 0
    if c == 0:
        return 0.0
    return c * log(v)

def lr_pof(k, n, p):
    # Kupiec proportion-of-failures statistic for k exceedances in n days
    ph = k / n
    return -2 * (xlogy(n - k, 1 - p) + xlogy(k, p) - xlogy(n - k, 1 - ph) - xlogy(k, ph))

def binom_cdf(n, q, k):
    # P(X <= k) for X ~ Binomial(n, q), built with the probability recurrence
    pmf = exp(n * log(1 - q))
    total = 0.0
    for j in range(0, k + 1):
        total += pmf
        pmf = pmf * (n - j) / (j + 1) * q / (1 - q)
    return total

def ind_stats(n00, n01, n10, n11):
    # Christoffersen independence test from the 2 x 2 transition counts
    pi01 = n01 / (n00 + n01)
    pi11 = n11 / (n10 + n11)
    pi = (n01 + n11) / (n00 + n01 + n10 + n11)
    null = xlogy(n00 + n10, 1 - pi) + xlogy(n01 + n11, pi)
    alt = xlogy(n00, 1 - pi01) + xlogy(n01, pi01) + xlogy(n10, 1 - pi11) + xlogy(n11, pi11)
    return [pi01, pi11, pi, null, alt, -2 * (null - alt)]

def reject_prob(n, p, qtrue):
    # Probability that the 5% Kupiec test rejects when the true hit rate is qtrue.
    # The statistic rises steeply above the null mean n * p, so every count beyond
    # kmax rejects and its probability is added as the leftover tail mass.
    kmax = floor(4 * n * p) + 10
    pmf = exp(n * log(1 - qtrue))
    total = 0.0
    mass = 0.0
    for k in range(0, kmax + 1):
        mass += pmf
        if lr_pof(k, n, p) > CRIT1:
            total += pmf
        pmf = pmf * (n - k) / (k + 1) * qtrue / (1 - qtrue)
    return total + (1 - mass)

# Step 1: the count under a correct model, and the Basel zones.
print("Expected exceedances:", round(t * p0, 4))
print("Expected exceedances at 95 percent:", round(t * 0.05, 4))
print("Exceedance standard deviation:", round(sqrt(t * p0 * (1 - p0)), 4))
print("Probability of zero exceedances:", round(binom_cdf(t, p0, 0), 4))
print("Exact probability of 7 or more:", round(1 - binom_cdf(t, p0, 6), 4))
green = binom_cdf(t, p0, 4)
print("Green zone probability:", round(green, 4))
print("Yellow zone probability:", round(binom_cdf(t, p0, 9) - green, 4))
print("Red zone probability:", round(1 - binom_cdf(t, p0, 9), 5))
if x <= 4:
    zone = "green"
elif x <= 9:
    zone = "yellow"
else:
    zone = "red"
print("Basel zone:", zone)

# Step 2: Kupiec proportion-of-failures test.
print("Observed exceedance rate:", round(x / t, 4))
ll0 = xlogy(t - x, 1 - p0) + xlogy(x, p0)
ll1 = xlogy(t - x, 1 - x / t) + xlogy(x, x / t)
print("Log-likelihood at correct coverage:", round(ll0, 4))
print("Log-likelihood at observed rate:", round(ll1, 4))
lrp = lr_pof(x, t, p0)
print("LR_pof:", round(lrp, 3))
reject1 = 0
if lrp > CRIT1:
    reject1 = 1
print("Kupiec rejects at 5 percent:", reject1)

# Step 3: Christoffersen independence test, 249 transitions with clustered hits.
c = ind_stats(238, 4, 4, 3)
print("Hit probability after a calm day:", round(c[0], 4))
print("Hit probability after a hit day:", round(c[1], 4))
print("Pooled hit probability:", round(c[2], 4))
print("Log-likelihood under independence:", round(c[3], 4))
print("Log-likelihood under Markov hits:", round(c[4], 4))
print("LR_ind:", round(c[5], 3))
reject2 = 0
if c[5] > CRIT1:
    reject2 = 1
print("Independence test rejects at 5 percent:", reject2)

# Step 4: conditional coverage.
lrcc = lrp + c[5]
print("LR_cc:", round(lrcc, 3))
reject3 = 0
if lrcc > CRIT2:
    reject3 = 1
print("Conditional coverage rejects at 5 percent:", reject3)
print("LR_pof on 249 days:", round(lr_pof(7, 249, p0), 3))

# Step 5: the same seven hits, all isolated.
d = ind_stats(235, 7, 7, 0)
print("Isolated LR_ind:", round(d[5], 3))
print("Isolated LR_cc:", round(lrp + d[5], 3))
reject4 = 0
if lrp + d[5] > CRIT2:
    reject4 = 1
print("Isolated conditional coverage rejects at 5 percent:", reject4)

# Step 6: size and power of the 5% Kupiec test.
print("LR_pof with no exceedances:", round(lr_pof(0, t, p0), 3))
print("Rejection probability when coverage is correct:", round(reject_prob(250, p0, 0.01), 4))
print("Power at true rate 2 percent, 250 days:", round(reject_prob(250, p0, 0.02), 4))
print("Green zone probability at true rate 2 percent:", round(binom_cdf(t, 0.02, 4), 4))
print("Power at true rate 2 percent, 1250 days:", round(reject_prob(1250, p0, 0.02), 4))""",
            'A second fictional desk reports a one-day 99% VaR for 250 days and has only 2 exceedances, on two consecutive days, so the 249 transitions are n00 = 246, n01 = 1, n10 = 1 and n11 = 1. Compute LR_pof, LR_ind and LR_cc, compare them with 3.841 and 5.991, and state the Basel zone. Then explain whether rejecting the model because of one consecutive pair is sound, and what you would check next.',
            'LR_pof = 2[2 ln(0.008/0.01) + 248 ln(0.992/0.99)] = 0.108, far below 3.841. For the transitions, π̂01 = 1/247 = 0.0040, π̂11 = 1/2 = 0.5 and π̂ = 2/249 = 0.0080, which gives LR_ind = 7.494, above 3.841, and LR_cc = 0.108 + 7.494 = 7.602, above 5.991. Two exceedances put the desk in the Basel green zone (0–4), so the traffic light passes it while the conditional-coverage test rejects it. The rejection rests on a single adjacent pair, which calls for caution but not dismissal: if two hits were placed at random among 250 days, the chance that they are adjacent is 249/31,125 = 0.8%, close to the asymptotic p-value of 0.006 for LR_ind, so the asymptotics are not misleading here. Still, one cluster is one event. Check what happened on those two days (a volatility jump the VaR did not anticipate, a data error, or a change in positions) and extend the sample before changing the model.',
            [
                q('A 99% VaR is backtested over T = 500 days with x = 12 exceedances. Using LR_pof = 2[x ln(x̂/p) + (T − x) ln((1 − x̂)/(1 − p))] with x̂ = x/T and p = 0.01, which conclusion is correct at the 5% level (critical value 3.841)?', ['LR_pof is about 7.1, so the hit rate is rejected', 'LR_pof is about 3.6, so the hit rate is not rejected', 'LR_pof is about 21.0, so the hit rate is rejected'], 0, 'x̂ = 12/500 = 0.024. LR_pof = 2[12 ln(2.4) + 488 ln(0.976/0.99)] = 2[10.506 − 6.950] = 7.11, which exceeds 3.841. The figure 3.6 forgets the factor 2, and 21.0 keeps only the exceedance term 2 × 12 × ln(2.4) and drops the term for the 488 days without a hit.'),
                q("Two desks each record 4 exceedances of a 99% VaR in 250 days. Desk X's hits form two adjacent pairs, with transition counts n01 = 2, n10 = 2 and n11 = 2. Desk Y's hits are four isolated days, with n01 = 4, n10 = 4 and n11 = 0. Which statistic tells the desks apart?", ['LR_pof, because it counts the exceedances', 'LR_ind, because the hit chance after a hit day, n11 / (n10 + n11), is 0.5 for desk X and 0 for desk Y', 'Neither, because both desks have the same hit count and the same Basel zone'], 1, 'LR_pof depends only on x = 4 and T = 250, and the Basel zone depends only on the count (green for both), so neither separates the desks. LR_ind uses the transition table: π̂11 = 2/(2 + 2) = 0.5 for desk X and 0/(4 + 0) = 0 for desk Y, so only LR_ind can flag the clustering in desk X.'),
                q("A desk's 99% VaR has no exceedances in 250 days. Which statement is correct?", ['The model is validated, because zero exceedances cannot indicate a problem', 'LR_pof is undefined at zero exceedances, so the Kupiec test cannot be run', 'The Basel zone is green, yet LR_pof = −2 × 250 × ln(0.99) = 5.03 exceeds 3.841, so the Kupiec test rejects a model that is too conservative'], 2, 'With x = 0 the term 0 ln 0 is taken as zero, so the observed-rate log-likelihood is 0 and LR_pof = −2 × 250 × ln(0.99) = 5.03, above 3.841. The test is two-sided: a 99% VaR that is never exceeded overstates risk. The Basel rule penalizes only too many exceptions, so it stays green. A correct model has no exceedances in 250 days with probability 0.99^250 = 0.081.'),
            ],
        ),
    ),
]

APPLICATIONS = [
    ('2.33', 'ldi', 'A liability is a dated stream of payments, so each payment should be discounted at the spot rate for its own date rather than at one blended yield.', "A fictional fund owes Rp 100 million in one year and Rp 100 million in three years. The one-year spot rate is 2.00% and the three-year spot rate is 4.57%. Compute the liability's present value with the curve and with one flat 4.57% rate, and say which payment the flat rate misvalues.", 'With the curve the value is 100/1.02 + 100/1.0457^3 = 98.04 + 87.45 = Rp 185.49 million; with one flat 4.57% it is 95.63 + 87.45 = Rp 183.08 million. The flat rate understates the liability by about Rp 2.41 million because it over-discounts the one-year payment. A correct curve still values only the promise: it says nothing about the collateral calls and spread moves that forced fund selling in the 2022 gilt episode, so it does not by itself make a hedge safe.'),
    ('2.34', 'parallel', 'Independent simulation batches can run on separate workers only if each batch owns a recorded random stream, and the reported error should come from the spread of batch results rather than from the core count.', 'A fictional desk splits one Monte Carlo valuation into four batches of 2,500 draws, each with its own recorded seed. The batch means are 6.91, 7.12, 6.83 and 7.02 per 100 of notional. Compute the pooled estimate and a standard error from the four batch means, and say what the spread implies for a single 2,500-draw batch.', "The pooled estimate is 6.97. The four batch means have a sample standard deviation of 0.127, which is the standard error of one 2,500-draw batch, and the pooled 10,000 draws have about 0.127/sqrt(4) = 0.063. Four batches make that spread a crude estimate, so keep each batch's seed identity and collect results by batch ID rather than finishing order. Batch spread captures sampling noise only; a model or discretization error shared by every batch would not show in it."),
    ('2.35', 'factors', "A fund's estimated alpha is signal plus noise, so the funds that look best also carry the most luck and should be pulled toward their peer group before any claim is made.", 'Four fictional funds report annual alpha estimates of 6, 2, 0 and −4 points, each with standard error 3. Compute the James–Stein factor and the shrunk estimates, and say whether the ranking changes.', 'The grand mean is 1 and S = 52, so the factor is 1 − 9 / 52 = 0.827 and the estimates are 5.13, 1.83, 0.17 and −3.13; the ranking is unchanged because one positive factor applies to every fund. With only four funds the improvement guarantee barely applies and the factor itself is noisy, and the method assumes exchangeable funds with independent errors, which funds sharing a style exposure violate.'),
    ('2.36', 'causal', 'When a district assigns training by lottery, the assignment itself supplies the exchangeability that an exact relabelling test needs, so no distributional assumption is required.', "A district randomly offers training to four of eight fictional shops. Treated shops' monthly sales growth is 6.0, 4.5, 5.2 and 3.9 points; untreated shops' growth is 3.1, 4.2, 2.8 and 3.6. Describe how to get the exact two-sided p-value from all 70 possible assignments, and state the smallest p-value this design can produce.", "Enumerate the 70 assignments, compute the difference in mean growth for each, and count those at least as extreme as the observed 1.475; four are, so p = 4/70 = 0.057, while the smallest possible value is 2/70 = 0.029. The test is exact for the sharp null that training changed no shop's growth because assignment was random, but it says nothing about spillovers between neighbouring shops, and eight shops can reject at 5% only when the groups do not overlap at all."),
    ('2.37', 'calibration', 'A probability above one-half is not automatically a decision to act. The threshold comes from what each error costs, and the probability itself has to be reliable in the population being scored.', "A fictional lender's logit gives a borrower a default probability of 0.06. Declining a loan that would have repaid costs 3 units of margin and approving one that defaults costs 45. Find the break-even probability and the decision, then the threshold if a missed default costs 90.", 'The break-even probability is 3/(3 + 45) = 0.0625, so a borrower at 0.06 is approved, but only just. If a missed default costs 90 the threshold falls to 3/93 = 0.0323 and the same borrower is declined. The comparison is only as good as the calibration: a model fitted on a book with a different default rate has a shifted intercept, so check calibration on the population that will actually be scored.'),
    ('2.38', 'factors', "A factor audit asks what common exposure sits behind a fund's active return. The fundamental law asks the forward version: how many independent bets could produce an information ratio, and do the signals share a hidden exposure that shrinks that number?", 'A fictional fund claims IC 0.05 on 200 stocks rebalanced twice a year, giving IR = 0.05 × √400 = 1.0. Its overweights share a value tilt, so the average bet-payoff correlation is 0.05. Compute the effective bets, the IR with correlated bets and the IR if the transfer coefficient is 0.7.', 'Effective bets are 200/(1 + 199 × 0.05) = 18.26 per rebalance, so annual breadth is 36.53 rather than 400 and IR = 0.05 × √36.53 = 0.302; with a transfer coefficient of 0.7 it is 0.212. The headline 1.0 overstates the expected ratio by more than three times before implementation losses and by about 4.7 times after them. The correlation must be estimated from payoffs, which is noisy with few dates, and one common correlation is a simplification; the factor audit is how to find out which shared exposure produces it.'),
    ('2.39', 'bi_rate', 'A policy-rate decision can prompt a relative view on two sectors, and the model forces that view to carry a size and a stated confidence before it moves any weight.', "A fictional two-fund market has equilibrium returns of 6% and 4%, and an analyst's relative view is that fund A beats fund B by 4 points. The prior variance of the view portfolio is 0.0016 and the view's own variance is 0.0009. Compute the posterior view return.", 'The equilibrium spread is 2 points and the view says 4. The view gets precision weight 0.0016 / (0.0016 + 0.0009) = 0.64, so the posterior spread is 2 + 0.64 × 2 = 3.28 points. A tighter margin of error would move it closer to 4, but that confidence has to be earned from a forecasting record rather than assumed, and the whole calculation inherits any error in the market-implied prior and the covariance matrix.'),
    ('2.40', 'calibration', "A VaR is a probability claim about exceedances, so its hit record is a calibration check on the model's one-percent promise.", 'A fictional 99% VaR has 4 exceedances in 250 days. Compute the expected count and the Kupiec statistic, compare it with 3.841, and say what the exceedance dates must show before the model is called sound.', 'The expected count is 2.5 and LR_pof = 2[4 ln(0.016/0.01) + 246 ln(0.984/0.99)] = 0.77, far below 3.841, and four exceedances sit in the Basel green zone. With 250 days the test has low power, so a pass is weak evidence; check whether the four dates cluster and what the market was doing on them, and remember the statistic says nothing about the size of the losses.'),
]
