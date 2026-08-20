# Experiment Log

## Project Question

Can property transaction prices be explained/predicted using
location, property type, tenure, new-build status and time?

## Project motivation

I'm hoping to improve my skills in random forests, regression
and just practice generally while working on a real project.

## Project database

House transaction prices in the UK in June of 2026.
The database is big enough (90k+) to find meaningful patterns and very recent.

## Initial Hypotheses

### H1 — Location matters
Properties closer to major urban centres should have higher prices.
While this is basically a given, I'm also planning to graph
it's effect per city.

### H2 — Property type matters
Detached properties should sell for more than flats, on average.

### H3 — New builds differ
New-build properties may have systematically different prices.

## Experiment 1 — Data Reduction

### Thought process

The raw dataset contains detailed address information which is unlikely
to be useful for the research question.
I've also deleted some data that might be necessary in

I decided that:
- exact street names are unnecessary
- transaction id is unnecessary
- secondary address text is unnecessary
- address number is unnecessary
- month/day are unnecessary
- record status is unnecessary
- locality for now will not be used

I cleaned up the dataset and we now have the following columns:
- price
- year
- postcode
- property type
- new build
- tenure
- town/city
- district
- county
- has secondary address

There is almost no missing data. Out of all rows only postcode has missing values.
It's missing 296 values out of 90k+ columns, so even that will hardly affect our research.

## Experiment 2 - First analyses

### Thought process

Before we create the models and everything, we have to understand the database.
I decided to make a few analyses.

### Mean price per Town/City
### Top 20 results by sample size.

                             mean  count
TownCity
LONDON               1.013438e+06   6300
MANCHESTER           3.034684e+05   1493
BRISTOL              4.378237e+05   1376
BIRMINGHAM           2.669195e+05   1347
NOTTINGHAM           3.476125e+05   1187
LIVERPOOL            2.515987e+05   1085
LEEDS                3.281927e+05    961
SHEFFIELD            3.014560e+05    872
LEICESTER            5.521895e+05    813
SOUTHAMPTON          4.636022e+05    692
NORWICH              3.341993e+05    677
NEWCASTLE UPON TYNE  2.659893e+05    642
PRESTON              2.663165e+05    590
DONCASTER            2.540647e+05    570
STOKE-ON-TRENT       2.124671e+05    565
READING              5.378295e+05    539
CARDIFF              3.134022e+05    539
DERBY                2.801024e+05    536
COVENTRY             3.501676e+05    511
YORK                 3.851772e+05    501

### Top 20 results by mean average price

TownCity
IVER                2.095027e+07      8
PURFLEET-ON-THAMES  3.145167e+06      6
AXMINSTER           2.708055e+06     29
AMBLESIDE           2.483580e+06     14
AYLESFORD           2.334265e+06     40
VIRGINIA WATER      2.333570e+06      5
MINDRUM             2.200000e+06      1
HAYES               2.048330e+06     87
SHEPPERTON          1.579176e+06     17
SOUTHALL            1.440470e+06     56
BRENTFORD           1.322435e+06     34
SALCOMBE            1.282805e+06      3
RADLETT             1.206706e+06     17
RINGWOOD            1.204401e+06     30
HINDHEAD            1.187672e+06     16
HENLEY-ON-THAMES    1.175388e+06     49
GODALMING           1.105821e+06     86
HERTFORD            1.099096e+06     55
EAST MOLESEY        1.094000e+06     13
BOREHAMWOOD         1.058508e+06     39

                      mean  count
PropertyType
O             1.274807e+06   5963   Other
D             5.038609e+05  20412   Detached
F             3.205157e+05  15992   Flat
S             3.182867e+05  24236   Semi-Detached
T             2.913846e+05  23684   Terraced

                                mean  count
District
CITY OF LONDON          5.671756e+06     22
CITY OF WESTMINSTER     3.223772e+06    331
CAMDEN                  2.418193e+06    281
KENSINGTON AND CHELSEA  2.069074e+06    217
TOWER HAMLETS           1.362033e+06    301
OXFORD                  1.003078e+06    149
HILLINGDON              9.844982e+05    333
HOUNSLOW                9.649022e+05    225
HARLOW                  9.368498e+05    123
RICHMOND UPON THAMES    9.004753e+05    284
LEICESTER               8.755925e+05    338
WAVERLEY                8.700817e+05    215
BUCKINGHAMSHIRE         8.637334e+05    793
MERTON                  8.521701e+05    239
TONBRIDGE AND MALLING   8.337103e+05    198
ELMBRIDGE               8.240976e+05    243
HERTSMERE               8.129099e+05    126
WANDSWORTH              8.107324e+05    576
HACKNEY                 8.056583e+05    295
WINDSOR AND MAIDENHEAD  7.999465e+05    212

              mean  count
Year
2023  1.119688e+06    531
2019  1.065561e+06    138
2021  1.034248e+06    408
2017  8.673967e+05    107
2024  8.260392e+05   1525
2018  6.644370e+05    120
2022  6.512677e+05    494
2020  5.189268e+05    240
2025  4.875834e+05  27485
2014  4.565090e+05     53
2015  4.524147e+05    107
2016  3.625784e+05    120
2026  3.601463e+05  57936
2013  3.232102e+05     50
2008  3.092196e+05     45
2010  3.044210e+05     31
2012  2.695842e+05     44
2005  2.613365e+05     61
2009  2.587447e+05     39
2006  2.513479e+05     68

### Summary of results

#### Cities

Out of the cities with most transactions, London stands out as the only one with a mean average of £1m+
When sorted by average mean price however, London didn't even make the list.
This, however, is not very reliable due to fairly low sample sizes.
Iver stands out with an incredibly high price of £20m+ but has an unreliable sample size.

#### Property Type

Semi-Detached, Terraced and Flats were all about £300k, whereas a Detached was meaningfully above that with £500k and the "Other" category was at a surprising £1.27m.

This data alone, however, is quite limited in giving a good understanding of the market. For example, you could imagine there being more flats in cities than in rural areas, which makes flats on average more valuable, even though a detached house could inherently be more valuable. These sorts of hypotheses will be tested later on.

#### District

Quite a few districts had good sample sizes (200+) and mean averages of 1m+ like Tower Hamlets, Kensington and Chelsea, Camden and City of Westminister

## Hypothesis : Idea, Test, Result (Price concerning location and property type)

### Idea

Flats are meaningfully less valuable than detached estates. The data supports this with (F=300k, D=500k), but I think the difference is bigger. My hypothesis is that there are MORE flats in cities, therefore on average they demand higher prices, but a detached house in that same city would be much more valuable.

### Test

To test this I simply sorted by City first, then by property type.

### Result

LONDON     D             2.670786e+06     85
           F             6.195076e+05   4037
           O             3.989065e+06    456
           S             1.291673e+06    363
           T             1.007210e+06   1359
MANCHESTER D             4.011037e+05    145
           F             2.326052e+05    390
           O             9.838234e+05     74
           S             2.918438e+05    469
           T             2.277701e+05    415

For more results take a look at city_property_type.md

Clearly on all of these 6 cities the Detached House is a lot more valuable than the Flats. This seems to mostly support my hypothesis, but we'll try to create a summary that looks at all cities.
Top 20 cities by sample size

           TownCity  Total Transactions  Detached Mean     Flat Mean   Difference  Detached vs Flat %
             LONDON                6300   2.670786e+06 619507.598464 2.051279e+06          331.114386
         MANCHESTER                1493   4.011037e+05 232605.202564 1.684985e+05           72.439690
            BRISTOL                1376   5.740781e+05 244302.220497 3.297759e+05          134.986849
         BIRMINGHAM                1347   4.534135e+05 172243.632653 2.811699e+05          163.239635
         NOTTINGHAM                1187   3.738173e+05 158684.484848 2.151328e+05          135.572670
          LIVERPOOL                1085   3.702350e+05 163199.272727 2.070357e+05          126.860678
              LEEDS                 961   5.059530e+05 172514.256579 3.334387e+05          193.281848
          SHEFFIELD                 872   4.328421e+05 146580.056180 2.862620e+05          195.293973
          LEICESTER                 813   4.230102e+05 145013.086420 2.779971e+05          191.704817
        SOUTHAMPTON                 692   5.447912e+05 201351.222222 3.434400e+05          170.567613
            NORWICH                 677   4.200626e+05 167886.486486 2.521761e+05          150.206323
NEWCASTLE UPON TYNE                 642   4.926011e+05 146403.204225 3.461979e+05          236.468773
            PRESTON                 590   3.925566e+05  99066.297297 2.934903e+05          296.256480
          DONCASTER                 570   3.218596e+05 117372.916667 2.044867e+05          174.219634
     STOKE-ON-TRENT                 565   3.069060e+05  83799.821429 2.231062e+05          266.237057
            READING                 539   8.532784e+05 230393.991379 6.228844e+05          270.356165
            CARDIFF                 539   5.357412e+05 170335.570312 3.654056e+05          214.521020
              DERBY                 536   3.639898e+05 135959.324324 2.280305e+05          167.719627
           COVENTRY                 511   4.610285e+05 137971.111111 3.230574e+05          234.148570
               YORK                 501   4.763548e+05 211069.084507 2.652857e+05          125.686663

### Summary

It seems that all major cities follow the expected result.
On average, detached properties have substantially higher transaction prices than flats across the largest cities in the dataset. However, this association cannot be interpreted as a causal effect of property type. Important omitted variables, particularly property size, may explain part of the observed difference.

* On average detached houses are much more valuable than flats.
* The exact reason for this is still up for debate and research.

## Experiment 4: Finishing the exploratory analysis

### Price by NewBuild

                   mean  count
NewBuild
N         418380.427612  83045
Y         398082.633112   7242

Tenure
F       437201.922828  68730
L       351553.040033  21557

The tenure result is quite interesting, but both (and especially)
the NewBuild results are very unreliable due to many possible
biases we haven't researched yet. For example, new-builds might
be concentrated more in major areas which would drive up price.

## Feature Engineering

Features:
['Year', 'PropertyType', 'NewBuild', 'Tenure', 'TownCity', 'District', 'County', 'HasSecondaryAddress']

Target:
Price

## Data Splitting

Training data:
(72229, 8)

Validation data:
(18058, 8)

## Linear Regression Baseline

The first model was a Linear Regression model using the available property characteristics:

* Year
* PropertyType
* NewBuild
* Tenure
* TownCity
* District
* County
* HasSecondaryAddress

Postcode was deliberately excluded from the initial model.

### Results

| Model                    | Mean Absolute Error | Within 20% of actual price |
| ----------------------   | ------------------: | -------------------------: |
| Linear Regression        |            £265,051 |                      31.5% |
| TownCity-only baseline   |            £260,948 |                      25.9% |
| Random Forest Regression |            £221,181 |                      45.0% |

The full Linear Regression model predicted house prices with a Mean Absolute Error of **£265,051**. Only **31.5%** of predictions fell within 20% of the actual transaction price.

As a simpler baseline, I also tested a model based purely on `TownCity`. Its MAE was **£260,948**, with only **25.9%** of predictions within 20% of the actual price.

This provides a useful baseline for testing whether more sophisticated models can capture relationships that Linear Regression cannot.

The Random Forest Regression model clearly had a much better accuracy of **45.0%**. Its MAE was **£221,181** which is also more precise by about £40,000

## Experiment 5 : Checking for accuracy per city.

### Linear Regression Model

                SampleSize            MAE  Within20Percent
TownCity
LONDON                1248  963226.396607         0.247596
BRISTOL                292  203295.030521         0.356164
MANCHESTER             276  153759.660241         0.286232
BIRMINGHAM             271  139779.444767         0.276753
NOTTINGHAM             247  179573.546670         0.267206
LIVERPOOL              236  198972.016171         0.199153
LEEDS                  204  151831.781221         0.215686
SHEFFIELD              174  193980.384763         0.172414
LEICESTER              157  892701.358505         0.267516
SOUTHAMPTON            151  274136.752600         0.251656
NORWICH                141  159138.477209         0.361702
PRESTON                120  126970.677174         0.291667
CARDIFF                109  122348.787871         0.321101
READING                108  359927.996636         0.259259
DONCASTER              106  113606.284031         0.433962

              SampleSize           MAE  Within20Percent
PropertyType
S                   4838  1.213450e+05         0.405333
T                   4788  1.242024e+05         0.332289
D                   3990  1.947034e+05         0.375188
F                   3186  2.423652e+05         0.175455
O                   1256  1.636551e+06         0.064490

City x property type
Top 20 results by sample size:

TownCity    PropertyType
LONDON      F                    789  4.730839e+05         0.253485
            T                    277  4.437848e+05         0.270758
BIRMINGHAM  T                     99  6.705349e+04         0.353535
MANCHESTER  S                     97  1.094162e+05         0.309278
LONDON      O                     95  6.618033e+06         0.084211
BRISTOL     T                     95  1.039858e+05         0.400000
LIVERPOOL   T                     90  8.710910e+04         0.277778
NOTTINGHAM  D                     85  1.747606e+05         0.282353
            S                     84  1.379494e+05         0.321429
MANCHESTER  T                     83  1.214314e+05         0.349398
BRISTOL     S                     78  1.266406e+05         0.397436
BIRMINGHAM  S                     76  8.127982e+04         0.447368
LEEDS       S                     71  1.132424e+05         0.197183
BRISTOL     F                     70  9.365530e+04         0.357143
LONDON      S                     68  4.848516e+05         0.352941
SHEFFIELD   S                     66  1.202509e+05         0.242424
MANCHESTER  F                     66  9.018436e+04         0.242424
LEEDS       T                     66  1.048945e+05         0.227273
BIRMINGHAM  F                     61  1.575723e+05         0.016393
LIVERPOOL   S                     59  9.482627e+04         0.288136
SHEFFIELD   T                     53  1.090530e+05         0.113208
NORWICH     D                     52  1.410377e+05         0.384615
LEICESTER   S                     51  1.546212e+05         0.411765
NOTTINGHAM  T                     50  1.293782e+05         0.300000
PRESTON     D                     47  1.190234e+05         0.382979
DONCASTER   S                     46  7.145004e+04         0.608696
HULL        T                     44  4.420133e+04         0.295455
SOUTHAMPTON F                     43  1.441442e+05         0.093023
COVENTRY    T                     43  8.728163e+04         0.232558
SOUTHAMPTON S                     43  2.847480e+05         0.418605

There are a few notable patterns
> Most cities seem to hang around 25-35% accuracy, but don't differ too much. Any differences might just aswell be attributed to random luck.
> Flats are much harder to predict than standalone houses
> The category "Other" has a very low accuracy, which makes sense since it doesn't tell much about the property at all.

These results are not very powerful yet. This model alone doesn't seem very promising.

### Random Forest Model

                SampleSize            MAE  Within20Percent
TownCity
LONDON                1248  882949.463624         0.346955
BRISTOL                292  192249.111971         0.424658
MANCHESTER             276  117559.500043         0.416667
BIRMINGHAM             271  102694.823206         0.464945
NOTTINGHAM             247   91470.749992         0.489879
LIVERPOOL              236  101448.976691         0.292373
LEEDS                  204  135494.893420         0.367647
SHEFFIELD              174  157647.892150         0.390805
LEICESTER              157  331843.570470         0.535032
SOUTHAMPTON            151  284175.636090         0.503311
NORWICH                141   99705.016811         0.482270
PRESTON                120   84270.641569         0.475000
CARDIFF                109   93262.487927         0.431193
READING                108  267628.706660         0.453704
DONCASTER              106   58391.288322         0.481132
DERBY                  106  115609.449360         0.405660
COVENTRY               106  158225.763205         0.566038
YORK                   106  195449.645511         0.462264
BRADFORD               105   82236.210821         0.419048
STOKE-ON-TRENT         100   68292.559822         0.520000
              SampleSize           MAE  Within20Percent
PropertyType
S                   4838  8.080493e+04         0.537412
T                   4788  8.812840e+04         0.482874
D                   3990  1.762972e+05         0.426065
F                   3186  1.161705e+05         0.419335
O                   1256  1.678066e+06         0.143312
                          SampleSize           MAE  Within20Percent
TownCity    PropertyType
LONDON      F                    789  2.704223e+05         0.359949
            T                    277  3.966651e+05         0.389892
BIRMINGHAM  T                     99  5.904629e+04         0.494949
MANCHESTER  S                     97  7.891309e+04         0.412371
LONDON      O                     95  7.354641e+06         0.094737
BRISTOL     T                     95  9.555803e+04         0.515789
LIVERPOOL   T                     90  6.161176e+04         0.322222
NOTTINGHAM  D                     85  1.002852e+05         0.447059
            S                     84  5.084116e+04         0.619048
MANCHESTER  T                     83  9.666205e+04         0.433735
BRISTOL     S                     78  1.166112e+05         0.448718
BIRMINGHAM  S                     76  7.349627e+04         0.565789
LEEDS       S                     71  7.831344e+04         0.366197
BRISTOL     F                     70  7.739771e+04         0.371429
LONDON      S                     68  5.467392e+05         0.397059
SHEFFIELD   S                     66  7.953693e+04         0.439394
MANCHESTER  F                     66  6.414556e+04         0.409091
LEEDS       T                     66  6.885005e+04         0.378788
BIRMINGHAM  F                     61  4.827995e+04         0.409836
LIVERPOOL   S                     59  9.310822e+04         0.271186
SHEFFIELD   T                     53  5.427689e+04         0.415094
NORWICH     D                     52  1.450080e+05         0.365385
LEICESTER   S                     51  5.046365e+04         0.705882
NOTTINGHAM  T                     50  5.165369e+04         0.460000
PRESTON     D                     47  1.246087e+05         0.404255
DONCASTER   S                     46  3.174413e+04         0.652174
HULL        T                     44  4.252414e+04         0.295455
SOUTHAMPTON F                     43  5.864086e+04         0.465116
COVENTRY    T                     43  4.627774e+04         0.581395
SOUTHAMPTON S                     43  7.914738e+04         0.604651

Noteworthy patterns:
> Most cities are around 50%, which is much better, but little difference across cities. Only Liverpool stands out a little with 29% accuracy
> This model has a much better F (flat) accuracy of 41.9% which is much better than 17% by the Linear Regression model.

## Grid Search Random Forest Predictions
Optimal ForesT: {'regressor__max_depth': None, 'regressor__min_samples_leaf': 5, 'regressor__n_estimators': 100}
Best cross-validation MAE:£204,213

Tuned Random Forest MAE: £213,915
Tuned RF predictions within 20: 44.4%
| Original Random Forest Regression |            £221,181 |                      45.0% |
| Tuned Random Forest               |            £213,915 |                      44.4% |

## Summary of Project

While this project has reinforced my programming skills, I am not very thrilled with the result.
My guess is that the biggest missing variable is the house size, which was not included in the original dataset.
Finetuning the random forest even more will probably give small results, if any.

My next project will be the same, but with a USA dataset that does include property size. I will put more effort into that and if it proves
much greater results, more easily I think it's fair to conclude that property size is a very important variable.