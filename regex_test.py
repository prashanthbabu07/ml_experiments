# %%

import re
# %%
test = re.findall(
    r'(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}', 'oct 21, 2014, Nov 11, 2015', re.IGNORECASE)

test
# %%

