<img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=200&section=header&text=오운완&fontSize=90" />

# 프로젝트 소개
**_"오늘 운동 완료하셨나요?"_**

>매년 연초에 1년짜리 헬스장 회원권을 끊고 사라진줄도 모르셨던 분들
>
>야식과 술로 얼룩진 허리둘레에 다이어트를 결심했지만 작심삼일로 끝난 분들
>
>그밖에 안좋은 생활패턴으로 건강을 챙기고 싶은 분들

하나라도 해당되신다면
간단한 운동부터 시작해볼까요?
꾸준히 할 수 있도록 저희가 도와드릴게요!

---
# 사용 스텍

## 백 엔드
<img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
<img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> 

## 버전
`Python 3.11`
`Django 4.2`
`Django Rest Framework 3.14`

## [프론트 엔드](https://github.com/rlfrhdiddl/A8ooo_fr)
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white">
<img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white"> 
<img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

## 프로젝트 관리, 배포
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=Git&logoColor=white">
<img src="https://img.shields.io/badge/Github-181717?style=for-the-badge&logo=Github&logoColor=white">
<img src="https://img.shields.io/badge/Visual Studio Code-007ACC?style=for-the-badge&logo=Visual Studio Code&logoColor=white">
<img src="https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=Gunicorn&logoColor=white">
<img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=NGINX&logoColor=white">
<img src="https://img.shields.io/badge/Amazon EC2-FF9900?style=for-the-badge&logo=Amazon EC2&logoColor=white">

---
# 프로젝트 구조
## 아키텍쳐
![](https://velog.velcdn.com/images/justyoon/post/6543815b-2c24-4bbc-937b-4d6b491025f0/image.png)

## ERD
![](https://github.com/jstyoon/TODAY-WORKOUT-DONE/assets/103176409/28136011-ab1d-4bc3-b2f1-38359dcf25a5)

---
# 서비스 플로우

## 회원기능
* 사용자는 오운완의 게시글을 열람할 수 있습니다. 
* 작성/댓글/수정/삭제/좋아요 등의 기능은 로그인을 요구합니다.
* 사용자는 회원가입 페이지에서 아이디,비밀번호,이메일을 입력하고 회원가입합니다.
  * 아이디,비밀번호,이메일은 작성조건이 있어 작성조건이 일치하지 않는다면 오류를 표시합니다.
  * 회원가입시 이메일 인증을 통해 가입할 수 있습니다. 비밀번호를 잊어버린 사용자는 이메일 인증을 통해 비밀번호 초기화가 가능합니다.
* 마이페이지에서 자신을 나타낼 수 있습니다.
	* 프로필 사진과 자기소개 등록이 가능합니다
	* 마이페이지 내에서도 비밀번호 변경이 가능합니다.
	* 회원 탈퇴가 가능합니다.


## 운동기록 기능
* 사용자는 운동내역을 작성하고 메인페이지 달력을 통해 운동기록을 시각화하여 볼 수 있습니다.
  * 운동을 계획한 날짜와 운동 완료상태에 따라 달력에 다르게 표시합니다.
* 공개/비공개를 선택하여 비공개의 글은 달력과 마이페이지에서만 확인이 가능하고, 공개 게시글은 피드에 공유됩니다.
* 왼쪽 위젯 속 오운완맨이 운동완료 횟 수에 따라 뛰는 속도가 달라집니다.


## 커뮤니티 기능
* 유저가 작성한 공개게시글은 커뮤니티로 자동 공유됩니다.
	* 게시글 좋아요 기능이 있습니다.
	* 댓글로 서로 소통하고, 댓글의 좋아요를 누를 수 있습니다.
  * 게시글과 댓글의 수정,삭제는 작성자 본인만 가능합니다.
* 달리기 액션이 `운동완료 갯수`에 따라 빨라집니다.
* `운동완료 갯수`를 기준으로 1~3등 유저는 피드페이지 상단 게시됩니다.



## 운동 추천 기능
* `위치정보 기반`(동의필요)으로 유저가 접속한 지역의 날씨 정보를 시간별로 최대 6시간 후 날씨를 1시간 단위로 보여줍니다.
  * 날씨가 맑은 경우 : 야외 운동 카테고리 중 랜덤으로 추천
  * 날씨가 안좋을 경우(눈, 비) : 실내 운동 카테고리 중 랜덤으로 추천

---
## 🎯팀원

이윤성 [Github] (https://github.com/jstyoon)  
나명흠 [Github] (https://github.com/rlfrhdiddl)  
박소진 [Github] (https://github.com/jinyjin7)  
방기호 [Github] (https://github.com/Tomatopizza)  
박종원 [Github] (https://github.com/Dabit0205)
---
