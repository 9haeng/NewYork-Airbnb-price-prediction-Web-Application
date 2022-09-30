# NewYork Airbnb price prediction web application
-----
![thumnail](https://user-images.githubusercontent.com/70729822/193028201-18646f04-9b8d-4bb7-9317-5278d73fd8ba.png)

에어비앤비 데이터셋 내 숙박 관련 데이터를 통한 숙박 가격을 예측하고, 입력한 조건에 맞는 숙소를 찾아주는 웹 애플리케이션 제작 프로젝트

[웹 애플리케이션](https://9haeng-ml-web-application-using-streamlit---init---haed2h.streamlitapp.com/) 을 직접 사용해보길 희망하신다면 링크를 클릭해주세요.


## 프로젝트 목표
----
`범주형, 숫자형 feature`를 활용해 숙박 가격 예측
최적의 모델을 활용해 웹 애플리케이션 배포

## 프로젝트 과정
웹 애플리케이션 배포를 제외한 모든 과정은 [지난 프로젝트](https://github.com/9haeng/NewYork-Airbnb-price-prediction) 에서 확인하실 수 있습니다.


## 웹 애플리케이션 구성
----
### 초기화면
![image](https://user-images.githubusercontent.com/70729822/193028956-245b5c43-4cfe-4c9d-8bc6-a74deb49a9c8.png)

간단한 서비스 가이드 메시지를 기재해 놓았습니다.

### 숙소 관련 옵션 선택
![options](https://user-images.githubusercontent.com/70729822/193029118-c749ab37-864a-4704-af73-662a4c368e5f.gif)

사용자는 본인의 관심 숙소와 관련된 옵션을 입력함으로써 더 정확한 예상 가격을 제공받을 수 있습니다.

### 입력 완료시 상태창
![summary](https://user-images.githubusercontent.com/70729822/193029599-87d8ac3a-025a-483c-bcfb-b55ea5bbc286.png)

사용자가 본인이 입력한 정보를 한 눈에 다시 확인할 수 있는 테이블을 제공합니다. 

이를 통해 사용자는 잘못 기입한 정보가 있는지, 수정할 요소가 있는지 확인할 수 있습니다.

### 드래그 바를 활용한 예측 활성화
![prediction](https://user-images.githubusercontent.com/70729822/193029168-a361958a-3ce1-48ba-a364-18de2bb4a78c.gif)

사용자는 요약 테이블 하단에 위치한 드래그 바를 우측으로 당김으로써 예상 가격을 제공받을 수 있습니다.

### 예상 가격 결과창
![result](https://user-images.githubusercontent.com/70729822/193029196-94e3b600-9ddd-4f9c-a123-2e0a421069be.png)

숙박 예상 가격은 달러 및 원으로 표기되며 원은 실시간 환율을 반영합니다.


또한 사용자의 관심 숙소 예상 가격을 예상하는데 영향을 미친 중요한 요소를 시각화해 제공합니다.

### 관심 숙소와 비슷한 숙소 알아보기
![website](https://user-images.githubusercontent.com/70729822/193030144-ffda61a2-7854-42ab-9909-4c2407923657.gif)

예상 가격을 확인한 후, 사용자는 본인의 관심 숙소와 비슷한 조건의 숙소를 실시간으로 확인할 수 있습니다.



