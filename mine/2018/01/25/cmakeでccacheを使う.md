<!--
id: b1d763c81e2b731c4f12
url: https://qiita.com/tenmyo/items/b1d763c81e2b731c4f12
created_at: 2018-01-25T12:30:10+09:00
updated_at: 2018-01-25T13:53:00+09:00
private: false
coediting: false
tags:
- CMake
- ccache
team: null
-->

# cmakeでccacheを使う

ccacheを使うとコンパイルの中間ファイルがキャッシュされ、２度め以降のコンパイルが速く終わります。

cmakeでのビルドで、ccacheを活用するにはどうしたらよいでしょうか。
よくあるのは`export CC='ccache gcc'`とかでコンパイラ自体をccacheに置き換える方法です。

cmakeにはコンパイル時にラッパを噛ませるための、[RULE_LAUNCH_COMPILE](https://cmake.org/cmake/help/v2.8.0/cmake.html#prop_global:RULE_LAUNCH_COMPILE)プロパティがあります。
このプロパティを使い、かつcmakeのオプションに対応したのが以下です。`ccmake`等で有効/無効を調整できるので、少し便利です。

```cmake:EnableCcache.cmake
option(CCACHE_ENABLE
  "If the command ccache is avilable, use it for compile."
  ON)
find_program(CCACHE_EXE ccache)
if(CCACHE_EXE)
  if(CCACHE_ENABLE)
    message(STATUS "Enable ccache")
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "${CCACHE_EXE}")
  endif()
endif()
```

cmake 3.4以降なら[CMAKE_\<LANG>_COMPILER_LAUNCHER](https://cmake.org/cmake/help/v3.4/variable/CMAKE_LANG_COMPILER_LAUNCHER.html)変数を使ったほうがよさそうです。
[Specify multiple RULE_LAUNCH_COMPILE will result in command line with semicolon (#17273) · Issues · CMake / CMake · GitLab](https://gitlab.kitware.com/cmake/cmake/issues/17273)

```cmake:EnableCcache.cmake(3.4以降)
option(CCACHE_ENABLE
  "If the command ccache is avilable, use it for compile."
  ON)
find_program(CCACHE_EXE ccache)
if(CCACHE_EXE)
  if(CCACHE_ENABLE)
    message(STATUS "Enable ccache")
    if(CMAKE_C_COMPILER_LAUNCHER)
      set(CMAKE_C_COMPILER_LAUNCHER "${CMAKE_C_COMPILER_LAUNCHER}" "${CCACHE_EXE}")
    else()
      set(CMAKE_C_COMPILER_LAUNCHER "${CCACHE_EXE}")
    endif()
    if(CMAKE_CXX_COMPILER_LAUNCHER)
      set(CMAKE_CXX_COMPILER_LAUNCHER "${CMAKE_CXX_COMPILER_LAUNCHER}" "${CCACHE_EXE}")
    else()
      set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_EXE}")
    endif()
  endif()
endif()
```
