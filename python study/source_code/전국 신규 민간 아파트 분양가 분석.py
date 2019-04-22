#!/usr/bin/env python
# coding: utf-8

# # 전국 신규 민간 아파트 분양가격 동향
# 
# 2015년 10월부터 2018년 7월까지의 전체 민간 신규아파트 분양가격 동향

# In[50]:


conda install -c conda-forge plotnine 


# In[52]:


conda install -c conda-forge missingno 


# In[56]:


import warnings
warnings.filterwarnings('ignore')


# In[58]:


import pandas as pd
import numpy as np
import re 
from plotnine import *


# %을 사용하면 터미널에서 사용할 수 있는 유닉스 명령어를 사용하실 수 있습니다. 경로를 불러오는 문제가 있을 때 이 방법을 사용하면 좋습니다.

# In[60]:


get_ipython().run_line_magic('pwd', '')


# In[62]:


# data 폴더 아래에 apt_price 라는 폴더를 만들어 공공데이터 포털에서 다운로드 받은 데이터를 모아 두었습니다. 해당 파일을 확인해 봅니다.
get_ipython().run_line_magic('ls', 'data\\apt_price')


# In[64]:


#데이터불러오기 (pre_sale에 넣어줬음)
pre_sale = pd.read_csv('data/apt_price/전국_평균_분양가격_2018.7월_.csv', encoding='euc-kr')
pre_sale.shape #불러온 데이터의 크기


# In[66]:


pre_sale.head() #위에서 5개의 데이터를 디폴트로. head(10) -> 10개가져옴


# In[68]:


pre_sale.tail() #뒤에서 5개 보여줌 


# In[70]:


# 데이터 프레임 요약해서 보여줌 ->
#분양가격이 숫자 타입이 아님. 숫자로 계산 할꺼니까 숫자 타입으로 변경하자.
pre_sale.info()


# In[88]:


#어떤 데이터 형태인지만 볼수 있음 
pre_sale.dtypes


# In[90]:


pre_sale.isnull().sum() #결측치 보여줌 (분양가격 결측치가 140 임)


# In[106]:


#44부터 48까지는 한글 안 깨지도록 하는 것 
import matplotlib


# In[107]:


from matplotlib import font_manager,rc


# In[108]:


font_name=font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()


# In[109]:


rc('font',family=font_name)


# In[110]:


matplotlib.rcParams['axes.unicode_minus']=False


# In[111]:


#결측치 보기->(missingno로 시각화 -> 분양가격 그래프에서 하얀 부분들이 결측치)
import missingno as msno
msno.matrix(pre_sale, figsize=(18,6))


# In[112]:


# 연도와 월은 카테고리 형태의 데이터이기 때문에 스트링 형태로 변경
pre_sale['연도'] = pre_sale['연도'].astype(str)
pre_sale['월'] = pre_sale['월'].astype(str)


# In[113]:


pre_sale_price = pre_sale['분양가격(㎡)']


# In[114]:


# 분양가격의 타입을 숫자로 변경해 '분양가격'이라는 새 컬럼 만들어서 넣어줌
pre_sale['분양가격'] = pd.to_numeric(pre_sale_price, errors='coerce')
# 평당 분양가격도 새로 만들어줌
pre_sale['평당분양가격'] = pre_sale['분양가격'] * 3.3


# In[115]:


pre_sale.info() #연도,월은 string으로 바꿔줘서 object로 바뀜.분양갸격과 평당분양가격이 float으로 새로 생김 


# In[116]:


pre_sale.dtypes


# In[117]:


# 분양가격 결측치가 늘어남->object여서 수치에 포함아 되지 않았던 공백란들도 숫자로 바꾸면서 결측치에 들어가게됨
pre_sale.isnull().sum()


# In[118]:


pre_sale.describe() #데이터 요약 (디폴트는 숫자형)


# In[119]:


#pre_sale.describe?


# In[120]:


pre_sale.describe(include=[np.object]) #object형도 describe


# In[121]:


# 2017년 데이터만 본다.
pre_sale_2017 = pre_sale.loc[pre_sale['연도'] == '2017'] #object타입이므로 ' ' 필요!
pre_sale_2017.shape


# In[122]:


# 같은 값을 갖고 있는 걸로 시도별로 동일하게 데이터가 들어 있는 것을 확인할 수 있다.
pre_sale['규모구분'].value_counts()


# In[123]:


pre_sale['지역명'].value_counts()


# # 전국평균 분양가격
# groupby 와 pivot_table 활용하기

# In[125]:


get_ipython().run_line_magic('pinfo', 'pre_sale.groupby')


# In[126]:


# 분양가격만 봤을 때(평균) 2015년에서 2018년으로 갈수록 오른 것을 확인할 수 있습니다.
pd.options.display.float_format = '{:,.0f}'.format
pre_sale.groupby(pre_sale.연도).describe().T 
#groupby 사용해서 연도별로 묶음, 
#describe의 기본값은 숫자여서 숫자인거만(분양가격,평당분양가격) 요약해서 나옴,
#(T 써서 x축과 y 바꿈->연도가 컬럼으로)


# # 규모별 전국 평균 분양가격

# In[127]:


get_ipython().run_line_magic('pinfo', 'pre_sale.pivot_table')


# In[128]:


pre_sale.pivot_table('평당분양가격', '규모구분', '연도') #디폴트는 (value,index,columns)임


# # 전국 분양가 변동금액
# 규모구분이 전체로 되어있는 금액으로 연도별 변동금액을 살펴봅니다.

# In[129]:


# 규모구분에서 전체로 되어있는 데이터만 가져온다.
region_year_all = pre_sale.loc[pre_sale['규모구분'] == '전체'] #loc->행 뽑음('전체'에 해당하는 모든 열 다 가져옴)
region_year = region_year_all.pivot_table('평당분양가격', '지역명', '연도').reset_index()
#index를 리셋해서 column의 rows(연도,지역명)를 하나로 만듦 
region_year


# In[130]:


region_year['변동액'] = (region_year['2018'] - region_year['2015']).astype(int)
max_delta_price = np.max(region_year['변동액'])*1000 #단위가 천원 단위라 1000곱해준거임
min_delta_price = np.min(region_year['변동액'])*1000
mean_delta_price = np.mean(region_year['변동액'])*1000

print('2015년부터 2018년까지 분양가는 계속 상승했으며, 상승액이 가장 큰 지역은 제주이며 상승액은 평당 {:,.0f}원이다.'.format(max_delta_price))
print('상승액이 가장 작은 지역은 울산이며 평당 {:,.0f}원이다.'.format(min_delta_price))
print('하지만 나중에 살펴보겠지만 울산에는 결측치가 많다. 따라서 변동액이 가장 작다라고 판단하기 어렵다.')
print('전국 평균 변동액은 평당 {:,.0f}원이다.'.format(mean_delta_price))

region_year


# -지금까지 2015년 10월에서 2018년 7월까지의 21개월간의 전국 신규 민간 아파트 분양가격 동향 파일을 요약함
# 
# -Pandas를 통해 데이터를 가져오고 요약해 보고 엑셀과 비슷하게 피봇테이블을 그려보기도 하고 groupby를 사용해서 데이터를 요약
# 

# # 시각화

# # 연도별 변동 그래프
# 공공데이터포털에서 제공하고 있는 평균 분양가격을 연도, 지역별로 그려보자

# In[133]:


(ggplot(region_year_all, aes(x='지역명', y='평당분양가격', fill='연도'))
 + geom_bar(stat='identity', position='dodge')
 + ggtitle('2015-2018년 신규 민간 아파트 분양가격')
 + theme(text=element_text(family=font_name),
        figure_size=(8, 4))
)


# # 지역별 평당 분양가격 합계
# -아래 데이터로 어느정도 규모로 분양사업이 이루어졌는지 보기 .
# 
# -전체 데이터로 봤을 때 서울, 경기, 부산, 제주에 분양 사업이 다른 지역에 비해 규모가 큰 것으로 보여지지만 분양가격대비로 나눠볼 필요 있음.

# In[135]:


pre_sale.pivot_table('평당분양가격', '규모구분', '지역명')


# ## 규모별

# In[137]:


# 서울의 경우 전용면적 85㎡초과 102㎡이하가 분양가격이 가장 비싸게 나옴.
(ggplot(pre_sale, aes(x='지역명', y='평당분양가격', fill='규모구분'))
 + geom_bar(stat='identity', position='dodge')
 + ggtitle('규모별 신규 민간 아파트 분양가격')
 + theme(text=element_text(family=font_name),
         figure_size=(8, 4))
)


# In[138]:


# 위에 그린 그래프 지역별로 나눠보기.
(ggplot(pre_sale)
 + aes(x='연도', y='평당분양가격', fill='규모구분')
 + geom_bar(stat='identity', position='dodge')
 + facet_wrap('지역명')
 + theme(text=element_text(family=font_name),
         axis_text_x=element_text(rotation=70),
         figure_size=(12, 12))
)


# In[139]:


# 박스플롯 그리기.
(ggplot(pre_sale, aes(x='지역명', y='평당분양가격', fill='규모구분'))
 + geom_boxplot()
 + ggtitle('전국 규모별 신규 민간 아파트 분양가격')
 + theme(text=element_text(family=font_name),
         figure_size=(12, 6))
)


# In[140]:


pre_sale_seoul = pre_sale.loc[pre_sale['지역명']=='서울']
(ggplot(pre_sale_seoul)
 + aes(x='연도', y='평당분양가격', fill='규모구분')
 + ggtitle('서울 연도/규모별 신규 민간 아파트 분양가격')
 + geom_boxplot()
 + theme(text=element_text(family=font_name))
)


# In[141]:


# 2015년에서 2018년까지 분양가 차이가 가장 컸던 제주
(ggplot(pre_sale.loc[pre_sale['지역명']=='제주'])
 + aes(x='연도', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + theme(text=element_text(family=font_name))
)


# In[142]:


# 2015년에서 2018년까지 분양가 차이가 가장 작았던 울산.
# 실제로는 분양가 차이가 적은 것이 아니라 결측치로 인해 분양가 차이가 적게 보인것이였음.
(ggplot(pre_sale.loc[pre_sale['지역명']=='울산'])
 + aes(x='연도', y='평당분양가격', fill='규모구분')
 + geom_boxplot()
 + theme(text=element_text(family=font_name))
)


# # Tidy Data 만들기
# ###### Tidy Data: 데이터 맞추기(데이터를 조작,모델링,시각화하기 편하게 만들어주는것)
# 
# 2013년 12월~2015년 9월 3.3㎡당 분양가격
# 
# 2015년 10월부터 2018년 4월까지 데이터는 평당 분양가로 조정을 해주었었는데 이 데이터는 평당 분양가가 들어가 있다.
# 
# 규모구분은 없으니까 지역,연도,월,분양가격을 맞춰주면 될것같음 

# In[146]:


df = pd.read_csv('data/apt_price/지역별_3.3㎡당_평균_분양가격_천원__15.09월.csv',                  encoding='euc-kr', skiprows=1, header=0) #윗줄의 필요없는 row하나 지움
df.shape


# In[209]:


# pandas에서 보기 쉽게 컬럼을 변경해 줄 필요가 있다.
df


# ##### 데이터 프레임 모습을 보고 가장 먼저 해야할 것은?
# 0,1번째 줄의 연과 월을 한줄로 합쳐주자
# 그런 다음 이전의 데이터와 같이 맞춰줘야하니까 연과 월을 두개의 칼럼으로 다시 나눠줘야함

# In[149]:


year = df.iloc[0]
month = df.iloc[1]
#행과 열 추출할땐:loc(명을 기준으로),iloc(index 기준으로)


# In[150]:


# 우선 year을 보자-> 많이 나온 결측치들을 채워준다.
year


# In[151]:


# 컬럼을 새로 만들어 주기 위해 0번째와 1번째 행을 합쳐준다.
for i, y in enumerate(year): 
    if i > 2 and i < 15:
        year[i] = ' '.join(['2014년', month[i]])
    elif i >= 15:
        year[i] = ' '.join(['2015년', month[i]])
    elif i == 2 :
        year[i] = ' '.join([year[i], month[i]])
    elif i == 1:
        year[i] = '시군구'
        
#for문처럼 반복되는 구간에서 객체가 현재 어느 위치에 있는지 알려주는 
#인덱스 값이 필요할때 enumerate 함수를 사용하면 매우 유용        
print(year)


# In[152]:


df.columns = year
#컬럼 지정 


# In[153]:


df = df.drop(df.index[[0,1]])
df


# In[154]:


# 지역 컬럼을 새로 만들어 시도와 시군구를 합쳐준다.
df['구분'] = df['구분'].fillna('')
df['시군구'] = df['시군구'].fillna('')


# In[155]:


df['지역'] = df['구분'] + df['시군구']


# In[156]:


df['지역']


# In[157]:


melt_columns = df.columns.copy()
melt_columns


# In[158]:


df_2013_2015 = pd.melt(df, id_vars=['지역'], value_vars=['2013년 12월', '2014년 1월', '2014년 2월', '2014년 3월',
       '2014년 4월', '2014년 5월', '2014년 6월', '2014년 7월', '2014년 8월',
       '2014년 9월', '2014년 10월', '2014년 11월', '2014년 12월', '2015년 1월',
       '2015년 2월', '2015년 3월', '2015년 4월', '2015년 5월', '2015년 6월',
       '2015년 7월', '2015년 8월', '2015년 9월'])
df_2013_2015.head()

#melt 사용법
#import pandas as pd
#df_b = pd.melt(df, id_vars=['A'], value_vars=['B', 'C'])
#df_a의 'A' 컬럼을 기준으로 두고 'B', 'C'는 variable 컬럼에 구분자로 넣고 
#'B', 'C' 컬럼의 값은 value 컬럼에 값으로 넣어 df_b 만들기


# In[159]:


df_2013_2015.columns = ['지역', '기간', '분양가']

df_2013_2015.head()


# In[160]:


df_2013_2015['연도'] = df_2013_2015['기간'].apply(lambda year_month : year_month.split('년')[0]) #기간에서 '년'이라는 단어로 split을 해서 0번째 값(ex) '2013')을 기간의 연도에 넣어줌 
df_2013_2015['월'] = df_2013_2015['기간'].apply(lambda year_month : re.sub('월', '', year_month.split('년')[1]).strip()) #년이랑 단어로 split해서 1번째 값( ex) ' 12월)을 공백이 있으니까 strip을 해서(ex) '12월') 월로 나눠서(ex) '12') 월에다가 넣어줌  

#ex)
#print(re.sub('\d{4}', 'XXXX', '010-1234-5678'))
#결과 010-XXXX-XXXX
#re.sub(정규표현식)은 패턴에 일치되는 문자열은 다른 문자열로 바꿔주는 것 (\d{4}'->'XXXX)


# In[161]:



df_2013_2015.head()


# ## 지역명 강원과 부산 정리

# In[163]:


df_2013_2015['지역'].value_counts()


# In[164]:


df_2013_2015['지역'] = df_2013_2015['지역'].apply(lambda x: re.sub('6대광역시부산','부산', x))
df_2013_2015['지역'] = df_2013_2015['지역'].apply(lambda x: re.sub('지방강원','강원', x))
df_2013_2015['지역'].value_counts()


# In[165]:


df_2013_2015.describe()


# In[166]:


df_2013_2015.info()


# In[167]:


df_2013_2015['분양가격'] = df_2013_2015['분양가'].str.replace(',', '').astype(int)


# ## 2013년 12월 부터 2015년 9월까지의 데이터 시각화 하기

# In[176]:


(ggplot(df_2013_2015, aes(x='지역', y='분양가격', fill='연도'))
 + geom_boxplot()
 + theme(text=element_text(family=font_name),
         figure_size=(12, 6))
)


# In[173]:


(ggplot(df_2013_2015, aes(x='지역', y='분양가격', fill='연도'))
 + geom_bar(stat='identity', position='dodge')
 + theme(text=element_text(family=font_name),
         figure_size=(12, 6))
)


# ## 이제 2013년부터 2018년 7월까지 데이터를 합칠 준비가 됨

# In[181]:


df_2015_2018 = pre_sale.loc[pre_sale['규모구분'] == '전체'] #2013~2015는 규모구분이 없어서 전체인거만 가져오기
print(df_2015_2018.shape)
df_2015_2018.head()


# In[182]:


df_2013_2015.columns


# In[183]:


df_2013_2015_prepare = df_2013_2015[['지역', '연도', '월', '분양가격']]
df_2013_2015_prepare.head()


# In[184]:



df_2013_2015_prepare.columns = ['지역명', '연도', '월', '평당분양가격']


# In[185]:


df_2015_2018.columns


# In[186]:


df_2015_2018_prepare = df_2015_2018[['지역명', '연도', '월', '평당분양가격']] #쓸 것만 가져오기
df_2015_2018_prepare.head()


# In[187]:


df_2015_2018_prepare.describe()


# In[188]:


df_2013_2018 = pd.concat([df_2013_2015_prepare, df_2015_2018_prepare]) #concat으로 위아래로 붙여주기
df_2013_2018.shape


# In[189]:


df_2013_2018.head()


# In[190]:


df_2013_2018.tail()


# In[191]:


df_2013_2015_region= df_2013_2015_prepare['지역명'].unique() #unique로 중복처리해서 고유값들만 보기 
df_2013_2015_region


# In[192]:


df_2015_2018_region = df_2015_2018_prepare['지역명'].unique()
df_2015_2018_region


# In[193]:


exclude_region = [region for region in df_2013_2015_region if not region in df_2015_2018_region] 
exclude_region 
#다른거 찾기


# In[194]:


df_2013_2018.shape


# In[195]:


df_2013_2018.loc[df_2013_2018['지역명'].str.match('전국|수도권')].head()


# In[197]:



df_2013_2018.drop(df_2013_2018.loc[df_2013_2018['지역명'].str.match('전국|수도권')].index, axis=0, inplace=True)
df_2013_2018.drop(df_2013_2018.loc[df_2013_2018['지역명'] == ''].index, axis=0, inplace=True)


# ## 2013년 12월~2018년 7월 전국 신규 민간 아파트 분양가격 동향 시각화

# In[199]:


(ggplot(df_2013_2018, aes(x='연도', y='평당분양가격'))
 + geom_bar(stat='identity', position='dodge')
 + theme(text=element_text(family=font_name))
)


# In[200]:


(ggplot(df_2013_2018, aes(x='지역명', y='평당분양가격', fill='연도'))
 + geom_bar(stat='identity', position='dodge')
 + theme(text=element_text(family=font_name),
         figure_size=(12, 6))
)


# In[201]:


(ggplot(df_2015_2018_prepare)
 + aes(x='연도', y='평당분양가격')
 + ggtitle('연도별 평당분양가격')
 + geom_boxplot()
 + theme(text=element_text(family=font_name))
)


# In[202]:


(ggplot(df_2013_2018)
 + aes(x='연도', y='평당분양가격')
 + ggtitle('연도별 평당분양가격')
 + geom_boxplot()
 + theme(text=element_text(family=font_name))
)


# In[206]:


df_2013_2018_jeju = df_2013_2018.loc[df_2013_2018['지역명'] == '제주']
(ggplot(df_2013_2018_jeju)
 + aes(x='연도', y='평당분양가격')
 + geom_boxplot()
 + theme(text=element_text(family=font_name))
)


# In[208]:


(ggplot(df_2013_2018)
 + aes(x='연도', y='평당분양가격')
 + geom_boxplot()
 + facet_wrap('지역명')
 + theme(text=element_text(family=font_name),
         axis_text_x=element_text(rotation=70),
         figure_size=(12, 12))
)

