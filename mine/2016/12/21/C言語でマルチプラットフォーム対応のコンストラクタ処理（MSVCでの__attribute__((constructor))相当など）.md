<!--
id: c3dd91af04d10d185a9a
url: https://qiita.com/tenmyo/items/c3dd91af04d10d185a9a
created_at: 2016-12-21T16:15:23+09:00
updated_at: 2016-12-21T16:17:59+09:00
private: false
coediting: false
tags:
- C
- GCC
- MSVC
team: null
-->

# C言語でマルチプラットフォーム対応のコンストラクタ処理（MSVCでの__attribute__((constructor))相当など）

# 背景
　最近いじっているCのソフトに、マルチプラットフォーム対応の静的なプラグイン機構[^1]をつけたくて、明示的に呼ばずに初期化処理を走らせる方法をいろいろ調べてみました。
　なおDLLやSOなどはエントリポイントがあるのでそちらを使ってもよいと思います。
[^1]: 既存コードに手を入れずに、作成したCソースファイルをビルドに含めるだけで、機能一覧に登録されるような機構。ユニットテスト作成時等にも便利。

# 解
1. C++に妥協し、static変数のコンストラクタを使う
2. `__attribute__((constructor))`を使う（gcc拡張）
3. `.CRT$X??`セクションに配置する（VCのCRT機能）

Stack Overflowの以下の回答がわかりやすいです。
[c - \_\_attribute__((constructor)) equivalent in VC? - Stack Overflow](http://stackoverflow.com/questions/1113409/attribute-constructor-equivalent-in-vc/2390626#2390626)

コードも抜粋しておきます。public domainなので、使いやすくてよいですね。

```initializer.c
    // Initializer/finalizer sample for MSVC and GCC/Clang.
    // 2010-2016 Joe Lowe. Released into the public domain.
#include <stdio.h>
#include <stdlib.h>

#ifdef __cplusplus
    #define INITIALIZER(f) \
        static void f(void); \
        struct f##_t_ { f##_t_(void) { f(); } }; static f##_t_ f##_; \
        static void f(void)
#elif defined(_MSC_VER)
    #pragma section(".CRT$XCU",read)
    #define INITIALIZER2_(f,p) \
        static void f(void); \
        __declspec(allocate(".CRT$XCU")) void (*f##_)(void) = f; \
        __pragma(comment(linker,"/include:" p #f "_")) \
        static void f(void)
    #ifdef _WIN64
        #define INITIALIZER(f) INITIALIZER2_(f,"")
    #else
        #define INITIALIZER(f) INITIALIZER2_(f,"_")
    #endif
#else
    #define INITIALIZER(f) \
        static void f(void) __attribute__((constructor)); \
        static void f(void)
#endif

static void finalize(void)
{
    printf( "finalize\n");
}

INITIALIZER( initialize)
{
    printf( "initialize\n");
    atexit( finalize);
}

int main( int argc, char** argv)
{
    printf( "main\n");
    return 0;
}
```

# 参考サイト（調査時の閲覧順）
* [main() の前に関数を呼ぶ - bkブログ](http://0xcc.net/blog/archives/000091.html)
gcc関係だとおそらく真っ先にヒットする解説ページ。arでリンクされなくなる問題への対処法（`--whole-archive`）も。

* [c - \_\_attribute__((constructor)) equivalent in VC? - Stack Overflow](http://stackoverflow.com/questions/1113409/attribute-constructor-equivalent-in-vc/2390626#2390626)
Stack Overflowでのやりとりとマルチプラットフォームのエレガントな回答

* [ブログズミ: C で main の前に関数コール](http://srz-zumix.blogspot.jp/2012/04/c-main.html)
テスティングフレームワークiutestを作成されている方の調査記事。
iutestはインクルードのみで利用できるらしく、なかなか便利そう。

* [MSDN : CRT の初期化](https://msdn.microsoft.com/ja-jp/library/bb918180.aspx)
VCの初期化の仕組み

* [Common Function Attributes - Using the GNU Compiler Collection (GCC)](https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html#Common-Function-Attributes)
gccのオンラインマニュアル
