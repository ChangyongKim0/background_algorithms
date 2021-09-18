# 제목 표현하기

# # 제목 1

## ## 제목 2

### ### 제목 3

<br></br>
<br></br>

# 글씨체

이텔릭체는 \*_별표(asterisks)_\*를 사용하세요.

볼드체는 \*\***별표(asterisks)**\*\*를 사용하세요.

<br></br>
<br></br>

# 리스트

- (- 순서가 필요하지 않은 목록)

1. (1. 순서가 필요한 목록)

1. (1. 순서가 필요한 목록)

   - (tab - 순서가 필요하지 않은 목록) (서브)
     - (tab tab - 순서가 필요하지 않은 목록) (서브)

1. (1. 순서가 필요한 목록)
   1. (tab 1. 순서가 필요한 목록) (서브)

<br></br>
<br></br>

# 코드

`'인라인 코드 (in-line type code)'` (') 대신 (`) 사용해야 함.

````javascript
// ```javascript
// 블록 타입 코드 block type code
// ```
const a = 1;
````

<br></br>
<br></br>

# 표

| 값         |                  의미                  |   기본값 |
| ---------- | :------------------------------------: | -------: |
| `static`   |     유형(기준) 없음 / 배치 불가능      | `static` |
| `relative` |       요소 자신을 기준으로 배치        |          |
| `absolute` | 위치 상 부모(조상)요소를 기준으로 배치 |          |
| `fixed`    |      브라우저 창을 기준으로 배치       |          |

```
값 | 의미 | 기본값
---|:---:|---:
`static` | 유형(기준) 없음 / 배치 불가능 | `static` |
`relative` | 요소 **자신**을 기준으로 배치 | |
`absolute` | 위치 상 **_부모_(조상)요소**를 기준으로 배치 | |
`fixed` | **브라우저 창**을 기준으로 배치 | |
```

<br></br>
<br></br>

# 인용문

> \> 인용문을 작성하세요!
>
> > \>> 중첩된 인용문(nested blockquote)을 만들 수 있습니다.
> >
> > > \>>> 중중첩된 인용문 1

> > > \>>> 중중첩된 인용문 2

> > > \>>> 중중첩된 인용문 3

<br></br>
<br></br>

# 수평선

\-\-\- (수평선)

---

<br></br>
<br></br>

# 수식

> (깃헙에서 자동으로 렌더하지 않아 추후 추가 예정.)

\$ $T:\cal C \to C$ \$ 이렇게 달러 표시를 사용.

\$\$

$$
T: \cal C \to C
$$

\$\$

모나드(monad)란 category $\cal C$ 에 대해 endofunctor $\cal C\to C$ 를 objectㄹ 갖고 이들 간의 natural transformation을 functo로 갖는 endofuntor category $\rm{End}(\cal C)$ 의 monoid를 말한다.

구체적으로, 모나드는 다음과 같이 구성된다.

> (원소) endofunctor $T:\cal C \to C$,

> (항등원) natural transformation $\eta: 1_{\cal C} \Rightarrow T$,

> (합성) natural tranformation $\mu: T^2 \Rightarrow T$.

이들은 임의의 대상 {\displaystyle A\in {\mathcal {C}}}A\in {\mathcal C}에 대하여 다음 세 그림들을 가환되게 하여야 한다.

> (결합 법칙) 임의의 대상 $A\in {\mathcal  C}$ 에 대하여, $T\mu _{A}\circ \mu _{A}=\mu _{{TA}}\circ \mu _{A}$ .  
> 즉, 다음 그림이 가환한다.
> $$ {\begin{matrix}TTTA&{\xrightarrow {T\mu }}&TTA\\{\scriptstyle \mu }\downarrow &&\downarrow \scriptstyle \mu \\TTA&{\xrightarrow[ {\mu }]{}}&TA\end{matrix}} $$

> (항등원의 성질) 임의의 대상 $A\in {\mathcal  C}$에 대하여, $\eta_{{TA}} \circ \mu_{A}=T\eta_{A} \circ \mu_{A}=\operatorname {id}_{A}$ .  
> 즉, 다음 두 그림이 가환한다.
> $${\begin{matrix}TA&{\xrightarrow  \eta }&TTA\\&{\scriptstyle \operatorname {id}}\searrow &\downarrow \scriptstyle \mu \\&&TA\end{matrix}}\qquad \qquad {\begin{matrix}TA&{\xrightarrow  {T\eta }}&TTA\\&{\scriptstyle \operatorname {id}}\searrow &\downarrow \scriptstyle \mu \\&&TA\end{matrix}}$$
