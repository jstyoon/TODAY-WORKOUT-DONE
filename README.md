<img src="https://capsule-render.vercel.app/api?type=waving&color=auto&height=200&section=header&text=오운완&fontSize=90" />

# 프로젝트 소개

**_"오늘 운동 완료하셨나요?"_**

> 매년 연초에 1년짜리 헬스장 회원권을 끊고 사라진줄도 모르셨던 분들
>
> 야식과 술로 얼룩진 허리둘레에 다이어트를 결심했지만 작심삼일로 끝난 분들
>
> 그밖에 안좋은 생활패턴으로 건강을 챙기고 싶은 분들

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

## [프론트 엔드 바로기](https://github.com/rlfrhdiddl/A8ooo_fr)

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

- 사용자는 오운완의 게시글을 열람할 수 있습니다.
- 작성/댓글/수정/삭제/좋아요 등의 기능은 로그인을 요구합니다.
- 사용자는 회원가입 페이지에서 아이디,비밀번호,이메일을 입력하고 회원가입합니다.
  - 아이디,비밀번호,이메일은 작성조건이 있어 작성조건이 일치하지 않는다면 오류를 표시합니다.
  - 회원가입시 이메일 인증을 통해 가입할 수 있습니다. 비밀번호를 잊어버린 사용자는 이메일 인증을 통해 비밀번호 초기화가 가능합니다.
- 마이페이지에서 자신을 나타낼 수 있습니다.
  - 프로필 사진과 자기소개 등록이 가능합니다
  - 마이페이지 내에서도 비밀번호 변경이 가능합니다.
  - 회원 탈퇴가 가능합니다.

## 운동기록 기능

- 사용자는 운동내역을 작성하고 메인페이지 달력을 통해 운동기록을 시각화하여 볼 수 있습니다.
  - 운동을 계획한 날짜와 운동 완료상태에 따라 달력에 다르게 표시합니다.
- 공개/비공개를 선택하여 비공개의 글은 달력과 마이페이지에서만 확인이 가능하고, 공개 게시글은 피드에 공유됩니다.
- 사용자가 글을 작성하면, 오른쪽 위젯이 만들어지며 위젯 속 오운완맨이 운동완료 횟 수에 따라 뛰는 속도가 달라집니다.

## 커뮤니티 기능

- 유저가 작성한 공개게시글은 커뮤니티로 자동 공유됩니다.
  - 게시글 좋아요 기능이 있습니다.
  - 댓글로 서로 소통하고, 댓글의 좋아요를 누를 수 있습니다.
  - 게시글과 댓글의 수정,삭제는 작성자 본인만 가능합니다.
- 달리기 액션이 `운동완료 횟수`에 따라 빨라집니다.
- `운동완료 횟수`를 기준으로 1~3등 유저는 피드페이지 상단 게시됩니다.

## 운동 추천 기능

- `위치정보 기반`(동의필요)으로 유저가 접속한 지역의 날씨 정보를 시간별로 최대 6시간 후 날씨를 1시간 단위로 보여줍니다.
  - 날씨가 맑은 경우 : 야외 운동 카테고리 중 랜덤으로 추천
  - 날씨가 안좋을 경우(눈, 비) : 실내 운동 카테고리 중 랜덤으로 추천

---

# 트러블 슈팅

<details>
<summary>article serializer 중복 코드</summary>
<div markdown="1">

## 문제
유저의 운동 완료 체크 수를 계산하여 메인페이지에 보여주는 위젯 구현

## 시도
시리얼라이저에서 데이터를 직렬화해줄때, 조건에 맞도록 유저의 운동 횟수를 카운트
```py
class ArticleViewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    check_status_count = serializers.SerializerMethodField()

        def get_check_status_count(self, obj):
        check_count = Articles.objects.filter(check_status=True, created_at__range=[date.today() - timedelta(days=10), date.today()])
        return check_count.count()

```
시리얼라이저에서 모델 데이터를 카운트할 경우 model에서 한번 가져오고, 
시리얼라이저에서 한번더 count를 위한 정보를 가져오므로 데이터를 2번 가져옴
이럴 경우 혹시 모를 에러 위험성이 높고, 데이터를 두번가져오는 것이 불필요하다 느꼈음

## 해결

```py
    @staticmethod
    def get_check_status_count(user):
        check_count = Articles.objects.filter(user=user, check_status=True)
        return check_count.count()
```
model에서 staticmethod를 이용해 count 함수를 추가해준 뒤 view에서 바로 처리해주도록 변경
serializer에서는 직렬화만 하고 데이터를 불필요하게 두번 가져오지 않게 됨.

</div>
</details>
<details>
<summary>쿠키 설정 문제</summary>
<div markdown="1">

## 문제
장고의 set_cookie 기능을 이용할 시 한글을 set_cookie할 때 latin-1코덱에 맞지 않는다는 에러.

## 시도
1.encode('utf-8')후 set_cookie. 이게 정답이었지만 print로 encode된 걸 출력했을 때 /b/368이런식으로 출력되는 것을 보고 오류인걸로 착각.
2.encode('utf-8')이후 decode('utf-8')을 시도 사실상 다시 한글을 set_cookie로 하는 것이라 latin-1형식에 맞지 않는다고 뜸.

## 해결
다시 encdoe('utf-8')을 하고 set_cookie를 한 뒤 프론트에서 어떻게 출력되는 지를 확인. 제대로 출력되는 것을 확인.

</div>
</details>
<details>
<summary>사용자의 위치정보 얻기</summary>
<div markdown="1">

## 문제
사용자의 위치정보를 얻어내고자 함.

## 시도

1.
백엔드에서 googlemaps를 오픈api를 이용해 위도와 경도를 구하려고 함. 
생각해보니 이건 백엔드가 돌아가는 곳의 위치를 알려주는 것이었고
서버에서 돌릴 경우 서버의 위치만 알려준다는 것을 알게됨.

2.
프론트에서 navigator.geolocation.getCurrentPosition을 이용해 위치를 구하려고 함.

```js
return new Promise((resolve, reject) => {
navigator.geolocation.getCurrentPosition(resolve, reject);
});
```

위치정보수집에 동의하면 제대로 위치정보를 얻는 다는 것을 확인함. 그러나 거부시 에러가 뜸.

## 해결
try {} catch(err){}를 이용해 에러가 떴을 때의 예외 처리를 통해 거부해도 오류가 나지 않게됨.

</div>
</details>
<details>
<summary>서버에서의 이메일 발송 문제</summary>
<div markdown="1">

## 문제
이메일 인증이 로컬에서는 되지만 서버에서는 되지 않음.

## 시도
1.
ec2의 보안규칙에서 인바운드 TCP 587포트를 열어줌.(이메일에서 쓰던 포트가 587이었기 때문.)
하지만 되지 않음. 그리고 어차피 서버에서 나가는 것은 아웃바운드이고 아웃바운드는 모두 열려있었기 때문에 의미가 없는 것이었음.

2.
gunicorn에 로거를 적용해 문제점을 파악해 보고자 함. 
SMTP 관련 에러를 뱉어내는 것을 확인. 
하지만 여전히 어떤 문제인지 파악하지 못함. 

3.
이번에는 print로 이메일 보내는 데 썼던 변수들을 출력해보기 위해 manage.py runserver 0.0.0.0:8000을 이용해 서버를 구동함.
  => 이메일이 발송이 됨.(??)
4.이번에는 로컬에서 8000포트가 아닌 다른 포트로 runserver를 해봄.
  => 여전히 이메일 발송이 잘 됨.

## 해결
EMAIL_HOST_PASSWORD, EMAIL_HOST_USER 등의 이메일 관련 변수들도 출력해봄.
EMAIL_HOST_PASSWORD는 .env에 저장돼 있는데 뒤에 #으로 주석이 붙어있었음. 
근데 주석까지 출력이 되는 것을 확인.
주석 제거후 이메일이 발송이 되는 것을 확인. 
gunicorn으로 서버를 구동시 manage.py runserver와는 다르게 manage.py를 거치지 않아 manage.py에 있는 dotenv.read_dotenv()가 동작하지 않고
아마도 파일 어디엔가 있는 .env를 읽는 코드로 읽고 있었을 것이라 추측됨.

</div>
</details>
<details>
<summary>좋아요 카운트 문제</summary>
<div markdown="1">

## 문제
좋아요 숫자가 올바르게 반영되지 않음
```py
class ArticleUpdateLikeCount(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        increment = request.data.get('increment', 0)
        article.save()
        return Response({"articleLikeCount": article.like_count}, status=status.HTTP_200_OK)
```

## 시도
좋아요인 increment를 js에서 조작하여 백엔드에서 저장하려고 시도 했다.
프론트에서 바꿔준 값을 백으로 보내서 저장하고 다시 돌려줘야 하는데 js에 미숙해서 구현하지 못 했다. 
```py
...
def post(self, request, article_id):
        article = get_object_or_404(Articles, id=article_id)
        fluctuation = article.likes.count()
        print(fluctuation)
        if not request.user.is_authenticated:
            return Response("로그인이 필요합니다.", status=status.HTTP_401_UNAUTHORIZED)
        else:
            if request.user in article.likes.all():
                fluctuation -= 1
                if fluctuation < 0:
                    fluctuation = 0
                article.like_count = fluctuation
                article.likes.remove(request.user)
                article.save()
                return Response({"message":"🤍", "fluctuation": article.like_count}, status=status.HTTP_200_OK)
            else:
                fluctuation += 1
                article.like_count = fluctuation
                article.likes.add(request.user)
                article.save()
                return Response({"message":"🧡", "fluctuation": article.like_count}, status=status.HTTP_200_OK)
...
```
## 해결
js로는 좋아요 이미지와 알러트만 띄워주었고,백엔드에서 좋아요 갯수가 변동되어 저장 할 수 있게 변경했다.

</div>
</details>
<details>
<summary>유저 이메일 인증시 데이터 로드 지연</summary>
<div markdown="1">

## 문제
유저 이메일 인증시 데이터 로드 지연

- 구현 테스트시 db삭제없이 유저모델 스키마를 활용하고자 기존 db를 dump, 그 db에서 일부만 변경해가며 load.
- 덤프와 로드를 반복하다보니 쌓인 데이터가 꽤나 많아졌고 똑같은 이메일 테스트를 해도 이전에는 느끼지 못한 전송 지연이 체감 되었다.
![image](https://github.com/jinyjin7/A8ooo/assets/103176409/11194ecc-7812-4493-90a3-ee0e863c8539)

## 시도
1. 이메일을 가진 유저 데이터가 많아서 조회가 늦어지는 것인가?
- 간단히 db를 일부 삭제후 postman test.
- 로드 시간이 줄어들긴 했지만 이런 단축이 유의미한 수치인지는 잘 모르겠다.
2. DB sqlite3의 이슈인가?
- 서버환경도 아니고 로컬환경에서 더미데이터가 많아졌다는게 sqlite3성능 문제라고 생각되지는 않았다
- 오히려 읽기 쓰기때 db조회에 작용하는 쿼리 문제같단 생각이 들었다.

## 해결
조회할 필드를 db_index=True로 변경후 새롭게 마이그레이션 해주었다.
처음에는 email만 확인했지만 username도 비슷한 이름이 많았고 
index를 적용해보니 1번 시도때와 비슷한 데이터량에도 응답이 빨라진 것을 알 수 있었다.

```py
    username = models.CharField(max_length=256, unique=True, db_index=True)
    email = models.EmailField(max_length=256, unique=True, db_index=True)
```

처음엔 단순한 호기심이었지만 index지정을 통해 full scan(테이블 전체를 조회)하지 않고 조회할 수 있다는 것을 알게 되었고 
앞으로 db 볼륨이 증가할 경우 테이블을 분리하여 디자인 패턴을 짜는 등 쿼리 성능을 염두해야겠다 느꼈다.
</div>
</details>

---

## 🎯팀원

이윤성 [Github] (https://github.com/jstyoon)
박소진 [Github] (https://github.com/jinyjin7)
나명흠 [Github] (https://github.com/rlfrhdiddl)
방기호 [Github] (https://github.com/Tomatopizza)
박종원 [Github] (https://github.com/Dabit0205)

---
