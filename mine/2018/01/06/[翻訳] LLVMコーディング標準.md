<!--
id: 7e4847b88e63d5769dd8
url: https://qiita.com/tenmyo/items/7e4847b88e63d5769dd8
created_at: 2018-01-06T15:19:28+09:00
updated_at: 2023-02-26T12:40:44+09:00
private: false
coediting: false
tags:
- C++
- LLVM
- 翻訳
- コーディング規約
- clang-format
team: null
-->

# [翻訳] LLVMコーディング標準(14.0.0)

# LLVMコーディング標準

LLVMは主にC++で実装されたコンパイラ基盤です。
近年急速に普及が進んでおり、RustやSwiftのバックエンドとしても利用されています。
LLVMの一部としてリリースされているCファミリーのコンパイラ`Clang`は、macOSやiOS、FreeBSD、OpenBSDの標準コンパイラとして採用されています。

本記事は、LLVMプロジェクトで用いられているコーディング標準（LLVM Coding Standards）のざっくり日本語訳です。
「組織内でのコーディング規約作成の参考にしたい」「`clang-format`等のフォーマッタでLLVMスタイルが指定できるが、その内容を知りたい」といった読者を想定しています。

LLVMのメジャーリリースに合わせてこの記事も更新していく予定です。現在は[14.0.0版](https://releases.llvm.org/14.0.0/docs/CodingStandards.html)に基づいています。原文の変更内容は[記事末尾](#原文の変更内容)に軽くまとめています。

解釈誤りや分かりづらさの指摘は、コメントや編集リクエストでいただけたら幸いです。

[原文のcurrent版はこちら](https://llvm.org/docs/CodingStandards.html)

----

<!--
Introduction
============
-->

## 前書き

<!--
This document describes coding standards that are used in the LLVM project.
Although no coding standards should be regarded as absolute requirements to be
followed in all instances, coding standards are
particularly important for large-scale code bases that follow a library-based
design (like LLVM).
-->

この文書ではLLVMプロジェクトで用いられるコーディング標準について説明します。「どんな場合も従うべき絶対要件」となるようなコーディング標準はありませんが、コーディング標準は（LLVMのような）ライブラリ構造の大規模コードベースにとって特に重要です。

<!--
While this document may provide guidance for some mechanical formatting issues,
whitespace, or other "microscopic details", these are not fixed standards.
Always follow the golden rule:

.. _Golden Rule:

    **If you are extending, enhancing, or bug fixing already implemented code,
    use the style that is already being used so that the source is uniform and
    easy to follow.**

Note that some code bases (e.g. ``libc++``) have special reasons to deviate
from the coding standards.  For example, in the case of ``libc++``, this is
because the naming and other conventions are dictated by the C++ standard.
-->

この文書はフォーマットや空白等の細かい指針も提供しますが、それらは絶対的な標準ではありません。どんな場合も以下の原則に従います。

**原則：既存コードを修正/拡張する場合は、ソースの追いやすさと均一化のために既存のスタイルを使う。**

一部のコードベースには本文書の標準から逸れる特別な理由があることに注意してください。たとえば `libc++` ですが、これは命名規則等がC++標準で定められているためです。

<!--
There are some conventions that are not uniformly followed in the code base
(e.g. the naming convention).  This is because they are relatively new, and a
lot of code was written before they were put in place.  Our long term goal is
for the entire codebase to follow the convention, but we explicitly *do not*
want patches that do large-scale reformatting of existing code.  On the other
hand, it is reasonable to rename the methods of a class if you're about to
change it in some other way.  Please commit such changes separately to
make code review easier.

The ultimate goal of these guidelines is to increase the readability and
maintainability of our common source base.
-->

コードベースにはここの命名規則等に従わないコードも含まれています。これは大量のコードを持ってきたばかりのためです。長期目標はコードベース全体が規則に沿うことですが、既存コードを大きく整形するパッチは明らかに**望んでいません**。一方、ほかの理由での変更時にそのクラスのメソッド名を直すことは合理的です。コードレビューしやすくするため、そういった変更はコミットを分けてください。

本ガイドラインの究極の目標は、私たちのコードベースの可読性と保守性を高めることです。

<!--
Languages, Libraries, and Standards
===================================
-->

### 言語、ライブラリ、および標準

<!--
Most source code in LLVM and other LLVM projects using these coding standards
is C++ code. There are some places where C code is used either due to
environment restrictions, historical restrictions, or due to third-party source
code imported into the tree. Generally, our preference is for standards
conforming, modern, and portable C++ code as the implementation language of
choice.
-->

全体としては、規格に準拠したモダンでポータブルなC++コードを実装言語とします。LLVMや関連プロジェクトのソースコードの大半はC++コードですが、いくつかの部位ではCコードが使われています。これは環境の制約、歴史的な制限、もしくはサードパーティ製コードの利用に由来しています。

<!--
C++ Standard Versions
---------------------
-->

### C++標準のバージョン

<!--
Unless otherwise documented, LLVM subprojects are written using standard C++14
code and avoid unnecessary vendor-specific extensions.

Nevertheless, we restrict ourselves to features which are available in the
major toolchains supported as host compilers (see :doc:`GettingStarted` page,
section `Software`).

Each toolchain provides a good reference for what it accepts:

* Clang: https://clang.llvm.org/cxx_status.html
* GCC: https://gcc.gnu.org/projects/cxx-status.html#cxx14
* MSVC: https://msdn.microsoft.com/en-us/library/hh567368.aspx
-->

特に記載がない限り、LLVMサブプロジェクトはC++14標準を用いて、また不要なベンダー拡張は避けて書かれています。

とはいえ、ホストコンパイラとしてサポートする主要なツールチェイン[^toolchain]で使える機能に限定しています。
（[Getting Started with the LLVM System](https://releases.llvm.org/14.0.0/docs/GettingStarted.html)の`Software`セクションも参照のこと）
[^toolchain]: 訳注：LLVM14.0.0ではClang 3.5、Apple Clang 6.0、GCC 5.1、Visual Studio 2019。

どのツールチェインも、サポートする言語機能の良い資料を提供しています。

- Clang: <https://clang.llvm.org/cxx_status.html>
- GCC: <https://gcc.gnu.org/projects/cxx-status.html#cxx14>
- MSVC: <https://msdn.microsoft.com/en-us/library/hh567368.aspx>[^MSVC_features]

[^MSVC_features]: 訳注：対応すると思われる日本語ページ <https://docs.microsoft.com/ja-jp/cpp/visual-cpp-language-conformance>

<!--
C++ Standard Library
--------------------
-->

### C++標準ライブラリ

<!--
Instead of implementing custom data structures, we encourage the use of C++
standard library facilities or LLVM support libraries whenever they are
available for a particular task. LLVM and related projects emphasize and rely
on the standard library facilities and the LLVM support libraries as much as
possible.
-->

カスタムデータ構造を作る代わりに、C++標準ライブラリやLLVMサポートライブラリできる限り活用してください。LLVMと関連プロジェクトでは、標準ライブラリとLLVMサポートライブラリをできるだけ重視し頼ります。

<!--
LLVM support libraries (for example, `ADT
<https://github.com/llvm/llvm-project/tree/main/llvm/include/llvm/ADT>`_)
implement specialized data structures or functionality missing in the standard
library. Such libraries are usually implemented in the ``llvm`` namespace and
follow the expected standard interface, when there is one.
-->

LLVMサポートライブラリ（たとえば[ADT](https://github.com/llvm/llvm-project/tree/main/llvm/include/llvm/ADT)）は、標準ライブラリに見当たらない特殊なデータ構造や機能を実装します。それらライブラリでは通常``llvm``名前空間で実装され、期待される標準インタフェース（あれば）に従います。

<!--
When both C++ and the LLVM support libraries provide similar functionality, and
there isn't a specific reason to favor the C++ implementation, it is generally
preferable to use the LLVM library. For example, ``llvm::DenseMap`` should
almost always be used instead of ``std::map`` or ``std::unordered_map``, and
``llvm::SmallVector`` should usually be used instead of ``std::vector``.
-->

C++とLLVMサポートライブラリ両方が似た機能を提供しており、C++実装を優先する特段の理由がない場合は、一般にLLVMライブラリをお勧めします。たとえば、たいていは`std::map`や`std::unordered_map`よりも`llvm::DenseMap`を、また`std::vector`ではなく`llvm::SmallVector`を使うべきです。

<!--
We explicitly avoid some standard facilities, like the I/O streams, and instead
use LLVM's streams library (raw_ostream_). More detailed information on these
subjects is available in the :doc:`ProgrammersManual`.

For more information about LLVM's data structures and the tradeoffs they make,
please consult `that section of the programmer's manual
<https://llvm.org/docs/ProgrammersManual.html#picking-the-right-data-structure-for-a-task>`_.
-->

I/Oストリームのようないくつかの標準機能はあえて避け、代わりにLLVMのストリームライブラリ（[raw_ostream](#raw_ostreamを使う)）を使います。これに関する詳細は[LLVM Programmer's Manual](https://releases.llvm.org/14.0.0/docs/ProgrammersManual.html)にあります。

LLVMのデータ構造とそのトレードオフについての詳細は、[Programmer's Manualの該当章](https://releases.llvm.org/14.0.0/docs/ProgrammersManual.html#picking-the-right-data-structure-for-a-task)を参照ください。

<!--
Guidelines for Go code
---------------

Any code written in the Go programming language is not subject to the
formatting rules below. Instead, we adopt the formatting rules enforced by
the `gofmt`_ tool.

Go code should strive to be idiomatic. Two good sets of guidelines for what
this means are `Effective Go`_ and `Go Code Review Comments`_.

.. _gofmt:
  https://golang.org/cmd/gofmt/

.. _Effective Go:
  https://golang.org/doc/effective_go.html

.. _Go Code Review Comments:
  https://github.com/golang/go/wiki/CodeReviewComments
-->

### Go言語のガイドライン

Go言語で記述されたコードは、以降の書式ルールの対象にはなりません。その代わりに、 [gofmt][_gofmt] ツールによる整形を採用しています。

Goコードは慣習に倣うよう努めてください。[Effective Go][_Effective Go] および [Go Code Review Comments][_Go Code Review Comments] の2つが良いガイドラインとなります。

[_gofmt]: https://golang.org/cmd/gofmt/
[_Effective Go]: https://golang.org/doc/effective_go.html
[_Go Code Review Comments]: https://github.com/golang/go/wiki/CodeReviewComments

<!--
Mechanical Source Issues
========================

Source Code Formatting
----------------------

Commenting
^^^^^^^^^^

Comments are important for readability and maintainability. When writing comments,
write them as English prose, using proper capitalization, punctuation, etc.
Aim to describe what the code is trying to do and why, not *how* it does it at
a micro level. Here are a few important things to document:
-->

## 機械的なソースの問題

### ソースコードのフォーマット

#### コメント

可読性と保守性を高めるため、コメントを入れてください。英文で、適切な句読点と大小文字で書いてください。コードがなにを行おうとしているのか、またなぜ（why）行おうとしているのかを説明することに焦点を絞り、微細に *どうやるか（how）* を書くことは避けてください。重要な事柄をいくつか示します。

<!--
.. _header file comment:

File Headers
""""""""""""

Every source file should have a header on it that describes the basic purpose of
the file. The standard header looks like this:

.. code-block:: c++

  //===-- llvm/Instruction.h - Instruction class definition -------*- C++ -*-===//
  //
  //                     The LLVM Compiler Infrastructure
  //
  // Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
  // See https://llvm.org/LICENSE.txt for license information.
  // SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
  //
  //===----------------------------------------------------------------------===//
  ///
  /// \file
  /// This file contains the declaration of the Instruction class, which is the
  /// base class for all of the VM instructions.
  ///
  //===----------------------------------------------------------------------===//
-->

##### ファイルのヘッダ

すべてのソースファイルには、ファイルの基本的な目的を説明するヘッダコメントが必要です。

```cpp:標準のファイルヘッダ
  //===-- llvm/Instruction.h - Instruction class definition -------*- C++ -*-===//
  //
  //                     The LLVM Compiler Infrastructure
  //
  // Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
  // See https://llvm.org/LICENSE.txt for license information.
  // SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
  //
  //===----------------------------------------------------------------------===//
  ///
  /// \file
  /// This file contains the declaration of the Instruction class, which is the
  /// base class for all of the VM instructions.
  ///
  //===----------------------------------------------------------------------===//
```

<!--
A few things to note about this particular format: The "``-*- C++ -*-``" string
on the first line is there to tell Emacs that the source file is a C++ file, not
a C file (Emacs assumes ``.h`` files are C files by default).

.. note::

    This tag is not necessary in ``.cpp`` files.  The name of the file is also
    on the first line, along with a very short description of the purpose of the
    file.

The next section in the file is a concise note that defines the license that the
file is released under.  This makes it perfectly clear what terms the source
code can be distributed under and should not be modified in any way.

The main body is a `Doxygen <http://www.doxygen.nl/>`_ comment (identified by
the ``///`` comment marker instead of the usual ``//``) describing the purpose
of the file.  The first sentence (or a passage beginning with ``\brief``) is
used as an abstract.  Any additional information should be separated by a blank
line.  If an algorithm is based on a paper or is described in another source,
provide a reference.
-->

1行目の "`-*- C++ -*-`" は、EmacsにソースファイルがCではなくC++であることを教えます（Emacsはデフォルトで `.h`ファイルをCとして扱います）。

:::note
このタグは、`.cpp`ファイルでは不要です。最初の行にはファイル名と短い説明があります。
:::

ファイルの次のセクションは、ファイルがどのライセンスの元でリリースされたかを簡潔に定義します。これにより、ソースコードがどのような条件の下で配布できるかが明確になります。そのため、どのような形であれ、変更してはいけません。

本体は[Doxygen](https://www.doxygen.nl/)コメント（通常の`//`ではなく`///`コメントで識別されます）にてファイルの目的を説明します。最初の一文（または`\brief`で始まる段落）は概要として使われます。追加情報は空白行で分けます。アルゴリズムの実装でベースとする論文や資料があれば、その参照を含めてください。

<!--
Header Guard
""""""""""""

The header file's guard should be the all-caps path that a user of this header
would #include, using '_' instead of path separator and extension marker. 
For example, the header file
``llvm/include/llvm/Analysis/Utils/Local.h`` would be ``#include``-ed as 
``#include "llvm/Analysis/Utils/Local.h"``, so its guard is 
``LLVM_ANALYSIS_UTILS_LOCAL_H``.
-->

##### ヘッダガード

ヘッダファイルのガードは、ユーザーが#includeで使うパスを大文字に変え、パス区切りや拡張子区切りを'_'へ変えたものにします。
たとえば、ヘッダファイル``llvm/include/llvm/Analysis/Utils/Local.h``は``#include "llvm/Analysis/Utils/Local.h"``となります。ですのでガードは``LLVM_ANALYSIS_UTILS_LOCAL_H``です。

<!--
Class overviews
"""""""""""""""

Classes are a fundamental part of an object-oriented design.  As such, a
class definition should have a comment block that explains what the class is
used for and how it works.  Every non-trivial class is expected to have a
``doxygen`` comment block.
-->

##### クラス概要

クラスはオブジェクト指向設計の基本要素です。そのため、クラス定義にはそのクラスが何に使われどのように働くかを説明するコメントブロックが必要です。すべての重要なクラスに`doxygen`コメントブロックが必要です。

<!--
Method information
""""""""""""""""""

Methods and global functions should also be documented.  A quick note about
what it does and a description of the edge cases is all that is necessary here.
The reader should be able to understand how to use interfaces without reading
the code itself.

Good things to talk about here are what happens when something unexpected
happens, for instance, does the method return null?
-->

##### メソッド情報

メソッドとグローバル関数も文書化してください。ここでは、何をするかについての簡単なメモや、エッジケースでの挙動の説明のみがあれば十分です。読者はコードを読まずとも使い方を理解できる必要があります。

想定外の事態に何が起きるかについて触れるとよいでしょう。たとえばメソッドがnullを返した場合など。

<!--
Comment Formatting
^^^^^^^^^^^^^^^^^^

In general, prefer C++-style comments (``//`` for normal comments, ``///`` for
``doxygen`` documentation comments).  There are a few cases when it is
useful to use C-style (``/* */``) comments however:

#. When writing C code to be compatible with C89.

#. When writing a header file that may be ``#include``\d by a C source file.

#. When writing a source file that is used by a tool that only accepts C-style
   comments.

#. When documenting the significance of constants used as actual parameters in
   a call. This is most helpful for ``bool`` parameters, or passing ``0`` or
   ``nullptr``. The comment should contain the parameter name, which ought to be
   meaningful. For example, it's not clear what the parameter means in this call:

Commenting out large blocks of code is discouraged, but if you really have to do
this (for documentation purposes or as a suggestion for debug printing), use
``#if 0`` and ``#endif``. These nest properly and are better behaved in general
than C style comments.
-->

#### コメント書式

通常は、C++スタイルのコメントを用います（普通のコメントに`//`、`doxygen`の文書化コメントに`///`）。以下のようにCスタイル（`/* */`）を用いたほうが良い場合もあります。

1. C89互換のCコードファイルを書く場合。
2. Cソースファイルから`#include`されるヘッダファイルを書く場合。
3. Cスタイルのコメントしか受け付けないツール向けのファイルを各場合。
4. 実引数での定数の意味を説明する場合。特に`bool`パラメータや`0`、`nullptr`で有用です。引数名（meaningfulである）を含めます。たとえば、この呼び出しでパラメータの意味は不明確です。

```cpp
Object.emitName(nullptr);
```

インラインのCスタイルコメントは意味を明確にします。

```cpp
Object.emitName(/*Prefix=*/nullptr);
```

大量のコードのコメントアウトがどうしても必要な場合（ドキュメント目的やデバッグプリント案等）は、 `#if 0`と`#endif`を使ってください。Cスタイルコメントよりもうまく働きます。

<!--
Doxygen Use in Documentation Comments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use the ``\file`` command to turn the standard file header into a file-level
comment.

Include descriptive paragraphs for all public interfaces (public classes,
member and non-member functions).  Avoid restating the information that can
be inferred from the API name.  The first sentence (or a paragraph beginning
with ``\brief``) is used as an abstract. Try to use a single sentence as the
``\brief`` adds visual clutter.  Put detailed discussion into separate
paragraphs.

To refer to parameter names inside a paragraph, use the ``\p name`` command.
Don't use the ``\arg name`` command since it starts a new paragraph that
contains documentation for the parameter.

Wrap non-inline code examples in ``\code ... \endcode``.

To document a function parameter, start a new paragraph with the
``\param name`` command.  If the parameter is used as an out or an in/out
parameter, use the ``\param [out] name`` or ``\param [in,out] name`` command,
respectively.

To describe function return value, start a new paragraph with the ``\returns``
command.
-->

#### ドキュメントコメントでのDoxygenの使用

`\file`コマンドを使い、標準のファイルヘッダをファイルレベルのコメントにします。

すべての公開インタフェース（publicクラス、メンバーと非メンバー関数）について説明する段落を含めます。API名を読み替えただけの記載は避けます。最初の一文（または`\brief`で始まる段落）は概要として使われます。`\brief`は目が滑るため、単一の文を使ってみてください。詳細な議論は段落を分けます。

段落内で引数名を参照するには、`\p name`コマンドを使います。新たな段落が始まってしまうため、`\arg name`コマンドは使わないでください。

複数行のコード例は、`\code ... \endcode`で囲います。

関数引数の文書化には、`\param name`コマンドを使い新しい段落を始めます。引数が出力や入出力として用いられる場合、それぞれ`\param [out] name`や`\param [in,out] name`コマンドを使います。

関数の戻り値の説明には、`\returns`コマンドを使い新たな段落を始めます。

<!--
A minimal documentation comment:

.. code-block:: c++

  /// Sets the xyzzy property to \p Baz.
  void setXyzzy(bool Baz);

A documentation comment that uses all Doxygen features in a preferred way:

.. code-block:: c++

  /// Does foo and bar.
  ///
  /// Does not do foo the usual way if \p Baz is true.
  ///
  /// Typical usage:
  /// \code
  ///   fooBar(false, "quux", Res);
  /// \endcode
  ///
  /// \param Quux kind of foo to do.
  /// \param [out] Result filled with bar sequence on foo success.
  ///
  /// \returns true on success.
  bool fooBar(bool Baz, StringRef Quux, std::vector<int> &Result);
-->

```cpp:最小限のドキュメントコメント
  /// Sets the xyzzy property to \p Baz.
  void setXyzzy(bool Baz);
```

```cpp:紹介した全機能を使うドキュメントコメント
  /// Does foo and bar.
  ///
  /// Does not do foo the usual way if \p Baz is true.
  ///
  /// Typical usage:
  /// \code
  ///   fooBar(false, "quux", Res);
  /// \endcode
  ///
  /// \param Quux kind of foo to do.
  /// \param [out] Result filled with bar sequence on foo success.
  ///
  /// \returns true on success.
  bool fooBar(bool Baz, StringRef Quux, std::vector<int> &Result);
```

<!--
Don't duplicate the documentation comment in the header file and in the
implementation file.  Put the documentation comments for public APIs into the
header file.  Documentation comments for private APIs can go to the
implementation file.  In any case, implementation files can include additional
comments (not necessarily in Doxygen markup) to explain implementation details
as needed.

Don't duplicate function or class name at the beginning of the comment.
For humans it is obvious which function or class is being documented;
automatic documentation processing tools are smart enough to bind the comment
to the correct declaration.
-->

ヘッダファイルと実装ファイルでドキュメントコメントを重複させないこと。公開APIのドキュメントコメントはヘッダファイルに入れてください。非公開APIのドキュメントコメントは、実装ファイルで結構です。どんな場合でも、実装ファイルには必要に応じて、実装の詳細を説明するための追加コメントを入れられます（Doxygen形式でなくても）。

コメントの先頭に関数名やクラス名をコピーしないでください。関数やクラスが文書化されていることは明らかであり、Doxygenはコメントを正しい宣言に対応付けられます。

<!--
Avoid:

.. code-block:: c++

  // Example.h:

  // example - Does something important.
  void example();

  // Example.cpp:

  // example - Does something important.
  void example() { ... }
-->

```cpp:避ける
// Example.h:

// example - Does something important.
void example();

// Example.cpp:

// example - Does something important.
void example() { ... }
```

<!--
Preferred:

.. code-block:: c++

  // Example.h:

  /// Does something important.
  void example();

  // Example.cpp:

  /// Builds a B-tree in order to do foo.  See paper by...
  void example() { ... }
-->

```cpp:優先
// Example.h:

/// Does something important.
void example();

// Example.cpp:

/// Builds a B-tree in order to do foo.  See paper by...
void example() { ... }
```

<!--
Error and Warning Messages
^^^^^^^^^^^^^^^^^^^^^^^^^^
-->

#### エラーと警告メッセージ

訳注：ユーザーに出力するメッセージの指針です。LLVM開発者がコーディング中、コンパイラ警告に直面した場合の振る舞いに関しては[別章](#コンパイラ警告はエラーと同様に扱う)に記載されています。

<!--
Clear diagnostic messages are important to help users identify and fix issues in
their inputs. Use succinct but correct English prose that gives the user the
context needed to understand what went wrong. Also, to match error message
styles commonly produced by other tools, start the first sentence with a
lower-case letter, and finish the last sentence without a period, if it would
end in one otherwise. Sentences which end with different punctuation, such as
"did you forget ';'?", should still do so.
-->

明確な診断メッセージは、ユーザーが入力の問題を特定して直すために重要です。簡潔で正しい英語の散文を用い、何を誤ったのかの理解に必要なコンテキストを示します。そして、ほかのツールでの一般的なエラーメッセージのスタイルに合わせるには、最初の文を小文字で始め、最後の文は（別のもので終わっている場合）ピリオドなしに終えます。ほかの句読点で終わる文、 "did you forget ';'?" などはそのままでよいでしょう。

<!--
For example this is a good error message:

.. code-block:: none

  error: file.o: section header 3 is corrupt. Size is 10 when it should be 20

This is a bad message, since it does not provide useful information and uses the
wrong style:

.. code-block:: none

  error: file.o: Corrupt section header.
-->

```text: 例：良いエラーメッセージ
error: file.o: section header 3 is corrupt. Size is 10 when it should be 20
```

```text: 例：悪いエラーメッセージ（スタイル違反＆有益な情報がない）
error: file.o: Corrupt section header.
```

<!--
As with other coding standards, individual projects, such as the Clang Static
Analyzer, may have preexisting styles that do not conform to this. If a
different formatting scheme is used consistently throughout the project, use
that style instead. Otherwise, this standard applies to all LLVM tools,
including clang, clang-tidy, and so on.
-->

他のコーディング標準と同じく、個別のプロジェクト、たとえばClang Static Analyzerなどでは、これに準拠していない既存のスタイルが含まれていることがあります。プロジェクト全体で一貫した別のスタイルが使われていれば、それを使います。それ以外では、この標準はすべてのLLVMツールに適用されます。clangやclang-tidyなども含みます。

<!--
If the tool or project does not have existing functions to emit warnings or
errors, use the error and warning handlers provided in ``Support/WithColor.h``
to ensure they are printed in the appropriate style, rather than printing to
stderr directly.

When using ``report_fatal_error``, follow the same standards for the message as
regular error messages. Assertion messages and ``llvm_unreachable`` calls do not
necessarily need to follow these same styles as they are automatically
formatted, and thus these guidelines may not be suitable.
-->

ツールやプロジェクトで警告やエラーを発行する既存の関数がない場合は、``Support/WithColor.h``で提供されるエラー/警告ハンドラを使って適切なスタイルで出力されるようにします。stderrには直接出力しません。

``report_fatal_error``を使う場合、通常のエラーメッセージと同様の基準に従ってください。アサーションメッセージと``llvm_unreachable``呼び出しでは自動でフォーマットされるため必ずしも同じスタイルに従う必要はなく、これらのガイドラインは当てはまらない場合があります。

<!--
``#include`` Style
^^^^^^^^^^^^^^^^^^

Immediately after the `header file comment`_ (and include guards if working on a
header file), the `minimal list of #includes`_ required by the file should be
listed.  We prefer these ``#include``\s to be listed in this order:

.. _Main Module Header:
.. _Local/Private Headers:

#. Main Module Header
#. Local/Private Headers
#. LLVM project/subproject headers (``clang/...``, ``lldb/...``, ``llvm/...``, etc)
#. System ``#include``\s

and each category should be sorted lexicographically by the full path.
-->

#### `#include`の形式

[ファイルヘッダのコメント](#ファイルのヘッダ)（およびヘッダファイルの場合はインクルードガード）直後に、そのファイルに[必要最低限の`#include`](#includeは最低限に)を並べます。`#include`は次の順に並べます。

1. メインモジュールヘッダ
1. ローカル/プライベートヘッダ
1. LLVMプロジェクト/サブプロジェクトのヘッダ（`clang/...`, `lldb/...`, `llvm/...`, ...）
1. システムの`#include`

パスは省略せず、カテゴリごとに辞書順で並べます。

<!--
The `Main Module Header`_ file applies to ``.cpp`` files which implement an
interface defined by a ``.h`` file.  This ``#include`` should always be included
**first** regardless of where it lives on the file system.  By including a
header file first in the ``.cpp`` files that implement the interfaces, we ensure
that the header does not have any hidden dependencies which are not explicitly
``#include``\d in the header, but should be. It is also a form of documentation
in the ``.cpp`` file to indicate where the interfaces it implements are defined.

LLVM project and subproject headers should be grouped from most specific to least
specific, for the same reasons described above.  For example, LLDB depends on
both clang and LLVM, and clang depends on LLVM.  So an LLDB source file should
include ``lldb`` headers first, followed by ``clang`` headers, followed by
``llvm`` headers, to reduce the possibility (for example) of an LLDB header
accidentally picking up a missing include due to the previous inclusion of that
header in the main source file or some earlier header file.  clang should
similarly include its own headers before including llvm headers.  This rule
applies to all LLVM subprojects.
-->

メインモジュールヘッダファイルは、`.h`ファイルで定義されたインタフェースを実装する`.cpp`ファイルに適用されます。この`#include`は、それがファイルシステムのどこにあるかにかかわらず、**最初に**includeされるべきです。`.cpp`ファイルが実装するインタフェースをファイル先頭でincludeすることにより、ヘッダ内の`#include`に含まれない依存関係がないことを確認できます。暗黙の依存関係があった場合、コンパイルエラーとなってくれます。また、`.cpp`の実装するインタフェースがどこで定義されているかを示す一種のドキュメントにもなります。

LLVMプロジェクトとサブプロジェクトのヘッダでは、同様の理由で具体性の高いものから順にグループ分けします。たとえば、LLDBはclangとLLVMに依存しclangはLLVMに依存します。そのため、LLDBのソースファイルは`lldb`、`clang`、`llvm`の順にヘッダファイルをインクルードします。これにより、LLDBヘッダファイルから必要なインクルードが漏れてしまう可能性を減らします。clangでも同様に、LLVMヘッダの前に独自ヘッダをインクルードします。このルールは、すべてのLLVMサブプロジェクトに適用されます。

<!--
.. _fit into 80 columns:
Source Code Width
^^^^^^^^^^^^^^^^^

Write your code to fit within 80 columns.

There must be some limit to the width of the code in
order to allow developers to have multiple files side-by-side in
windows on a modest display.  If you are going to pick a width limit, it is
somewhat arbitrary but you might as well pick something standard.  Going with 90
columns (for example) instead of 80 columns wouldn't add any significant value
and would be detrimental to printing out code.  Also many other projects have
standardized on 80 columns, so some people have already configured their editors
for it (vs something else, like 90 columns).
-->

#### ソースコードの幅

80桁に収めてください。

ディスプレイに複数のファイルを並べて表示するために、コード幅にはある程度の制限が必要です。その選択においては、多少恣意的ですが標準的なものを選ぶべきです。80桁の代わりたとえば90桁にしても、大した価値も得られず印刷にも不便です。また多くの他プロジェクトでは80桁が採用されているため、みなエディタをそのように設定しています。

<!--
Whitespace
^^^^^^^^^^^^^^^^^^^^^^^^^^

In all cases, prefer spaces to tabs in source files.  People have different
preferred indentation levels, and different styles of indentation that they
like; this is fine.  What isn't fine is that different editors/viewers expand
tabs out to different tab stops.  This can cause your code to look completely
unreadable, and it is not worth dealing with.

As always, follow the `Golden Rule`_ above: follow the style of existing code
if you are modifying and extending it.

Do not add trailing whitespace.  Some common editors will automatically remove
trailing whitespace when saving a file which causes unrelated changes to appear
in diffs and commits.
-->

#### 空白

ソースファイルではタブよりもスペースがよいです。タブは表示環境ごとに異なるタブストップで展開され崩れる恐れがあります。

いつものように[原則](#前書き)に従いましょう。既存コードに手を入れる場合、既存のスタイルに準じます。

末尾空白（`trailing whitespace`）を追加しないでください。 よくあるエディタはファイル保存時に末尾の空白を自動的に削除するため、差分とコミットに無関係な変更が現れてしまいます。

<!--
Format Lambdas Like Blocks Of Code
""""""""""""""""""""""""""""""""""

When formatting a multi-line lambda, format it like a block of code. If there
is only one multi-line lambda in a statement, and there are no expressions
lexically after it in the statement, drop the indent to the standard two space
indent for a block of code, as if it were an if-block opened by the preceding
part of the statement:

.. code-block:: c++

  std::sort(foo.begin(), foo.end(), [&](Foo a, Foo b) -> bool {
    if (a.blah < b.blah)
      return true;
    if (a.baz < b.baz)
      return true;
    return a.bam < b.bam;
  });
-->

##### ラムダはコードブロックと同様に整形

複数行のラムダは、コードブロックと同様に整形してください。もし文中に複数行のラムダひとつしかなく、その後に式もない場合、ifブロック同様にインデントを下げます。

```cpp
std::sort(foo.begin(), foo.end(), [&](Foo a, Foo b) -> bool {
  if (a.blah < b.blah)
    return true;
  if (a.baz < b.baz)
    return true;
  return a.bam < b.bam;
});
```

<!--
To take best advantage of this formatting, if you are designing an API which
accepts a continuation or single callable argument (be it a function object, or
a ``std::function``), it should be the last argument if at all possible.

If there are multiple multi-line lambdas in a statement, or additional
parameters after the lambda, indent the block two spaces from the indent of the
``[]``:
-->

このフォーマットを活かすため、新規APIで継続や単一の呼び出し可能な引数（関数オブジェクトや`std::function`）をとる場合、なるべく最後の引数にします。

文の中にいくつも複数行のラムダがあったり、ラムダの後ろに追加パラメータがある場合には、`[]`から2スペースインデントします。

<!--
.. code-block:: c++

  dyn_switch(V->stripPointerCasts(),
             [] (PHINode *PN) {
               // process phis...
             },
             [] (SelectInst *SI) {
               // process selects...
             },
             [] (LoadInst *LI) {
               // process loads...
             },
             [] (AllocaInst *AI) {
               // process allocas...
             });
-->

```cpp
dyn_switch(V->stripPointerCasts(),
           [] (PHINode *PN) {
             // process phis...
           },
           [] (SelectInst *SI) {
             // process selects...
           },
           [] (LoadInst *LI) {
             // process loads...
           },
           [] (AllocaInst *AI) {
             // process allocas...
           });
```

<!--
Braced Initializer Lists
""""""""""""""""""""""""

Starting from C++11, there are significantly more uses of braced lists to
perform initialization. For example, they can be used to construct aggregate
temporaries in expressions. They now have a natural way of ending up nested
within each other and within function calls in order to build up aggregates
(such as option structs) from local variables.
-->

##### ブレース初期化子リスト

C++11以降、初期化でのブレースリスト利用が大幅に増えています。たとえば、式内で一時的な集約を作るために使えます。ローカル変数から集約（オプション構造体等）を作るために、お互いの入れ子や関数呼び出し内で無理なく完結します。

<!--
The historically common formatting of braced initialization of aggregate
variables does not mix cleanly with deep nesting, general expression contexts,
function arguments, and lambdas. We suggest new code use a simple rule for
formatting braced initialization lists: act as-if the braces were parentheses
in a function call. The formatting rules exactly match those already well
understood for formatting nested function calls. Examples:

.. code-block:: c++

  foo({a, b, c}, {1, 2, 3});

  llvm::Constant *Mask[] = {
      llvm::ConstantInt::get(llvm::Type::getInt32Ty(getLLVMContext()), 0),
      llvm::ConstantInt::get(llvm::Type::getInt32Ty(getLLVMContext()), 1),
      llvm::ConstantInt::get(llvm::Type::getInt32Ty(getLLVMContext()), 2)};

This formatting scheme also makes it particularly easy to get predictable,
consistent, and automatic formatting with tools like `Clang Format`_.

.. _Clang Format: https://clang.llvm.org/docs/ClangFormat.html
-->

変数をまとめて初期化するブレースの歴史的な共通フォーマットは、深いネスト、一般的な式中、関数引数、およびラムダときれいに混在できません。私たちは、新しいコードでブレース初期化リストの簡単な規則を用いることを提案します。関数呼び出し内のブレースは通常の括弧と同様に扱います。このフォーマット規則は、すでによく知られたネストされた関数呼び出しのフォーマットとうまく整合します。

```cpp:例
foo({a, b, c}, {1, 2, 3});

llvm::Constant *Mask[] = {
    llvm::ConstantInt::get(llvm::Type::getInt32Ty(getLLVMContext()), 0),
    llvm::ConstantInt::get(llvm::Type::getInt32Ty(getLLVMContext()), 1),
    llvm::ConstantInt::get(llvm::Type::getInt32Ty(getLLVMContext()), 2)};
```

このフォーマット方式は、適用が簡単で、一貫性があり、[Clang Format](https://clang.llvm.org/docs/ClangFormat.html)のようなツールで自動整形できます。

<!--

Language and Compiler Issues
----------------------------

Treat Compiler Warnings Like Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Compiler warnings are often useful and help improve the code.  Those that are
not useful, can be often suppressed with a small code change. For example, an
assignment in the ``if`` condition is often a typo:

.. code-block:: c++

  if (V = getValue()) {
    ...
  }
-->

### 言語とコンパイラの問題

#### コンパイラ警告はエラーと同様に扱う

コンパイラ警告はたいていコードの改善に役立ちます。役に立たないものは、多くの場合コードを少し変えるだけで抑えられます。たとえば、`if`条件での代入はたいていtypoです。

```cpp
if (V = getValue()) {
  ...
}
```

<!--
Several compilers will print a warning for the code above. It can be suppressed
by adding parentheses:

.. code-block:: c++

  if ((V = getValue())) {
    ...
  }

which shuts ``gcc`` up.  Any ``gcc`` warning that annoys you can be fixed by
massaging the code appropriately.
-->

いくつかのコンパイラは上記のコードに警告します。括弧を足せば抑えられます。

```cpp
if ((V = getValue())) {
  ...
}
```

<!--
Write Portable Code
^^^^^^^^^^^^^^^^^^^

In almost all cases, it is possible to write completely portable code.  When
you need to rely on non-portable code, put it behind a well-defined and
well-documented interface.
-->

#### 移植性のあるコードを書く

ほとんどの場合、完全に移植性のあるコードを書けます。移植性のないコードに頼らざるを得ない場合は、明確に定義されよく文書化されたインタフェースの背後に置きます。

<!--
Do not use RTTI or Exceptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In an effort to reduce code and executable size, LLVM does not use exceptions
or RTTI (`runtime type information
<https://en.wikipedia.org/wiki/Run-time_type_information>`_, for example,
``dynamic_cast<>``).

That said, LLVM does make extensive use of a hand-rolled form of RTTI that use
templates like :ref:`isa\<>, cast\<>, and dyn_cast\<> <isa>`.
This form of RTTI is opt-in and can be
:doc:`added to any class <HowToSetUpLLVMStyleRTTI>`.
-->

#### RTTIや例外を使わない

コードと実行ファイルのサイズを減らすために、LLVMでは例外やRTTI（[実行時型情報](https://ja.wikipedia.org/wiki/%E5%AE%9F%E8%A1%8C%E6%99%82%E5%9E%8B%E6%83%85%E5%A0%B1)、たとえば`dynamic_cast<>`）は使いません。

とはいえ、LLVMではRTTIを手で展開した [isa\<>、cast\<>、そしてdyn_cast\<>](https://releases.llvm.org/14.0.0/docs/ProgrammersManual.html#isa) のようなテンプレートを広く用います。RTTIのこの形式は、[任意のクラス](https://releases.llvm.org/14.0.0/docs/HowToSetUpLLVMStyleRTTI.html)にオプトインで追加できます。

<!--
.. _static constructor:
Do not use Static Constructors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Static constructors and destructors (e.g., global variables whose types have a
constructor or destructor) should not be added to the code base, and should be
removed wherever possible.

Globals in different source files are initialized in `arbitrary order
<https://yosefk.com/c++fqa/ctors.html#fqa-10.12>`, making the code more
difficult to reason about.

Static constructors have negative impact on launch time of programs that use
LLVM as a library. We would really like for there to be zero cost for linking
in an additional LLVM target or other library into an application, but static
constructors undermine this goal.
-->

#### 静的コンストラクタを使わない

静的コンストラクタとデストラクタ（たとえば、コンストラクタやデストラクタを持つ型のグローバル変数）はコードベースに追加されるべきではなく、可能な限り除かなければなりません。

異なるソースファイル内のグローバル変数は[任意の順序](https://yosefk.com/c++fqa/ctors.html#fqa-10.12)で初期化されるため、コードの推測が難しくなります。

静的コンストラクタは、LLVMをライブラリとして使うプログラムの起動時間に悪影響を及ぼします。私たちは、追加のLLVMターゲットやアプリケーションのライブラリへのリンクがゼロコストであることを強く望みますが、静的コンストラクタはこの目標を覆します。

<!--
Use of ``class`` and ``struct`` Keywords
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In C++, the ``class`` and ``struct`` keywords can be used almost
interchangeably. The only difference is when they are used to declare a class:
``class`` makes all members private by default while ``struct`` makes all
members public by default.
-->

#### `class`と`struct`キーワードの使い方

C++では、`class`と`struct`キーワードはほぼ同じ意味で使えます。唯一の違いはクラス宣言の場合です。`class`はデフォルトでメンバーがprivateですが、`struct`はpublicです。

<!--
* All declarations and definitions of a given ``class`` or ``struct`` must use
  the same keyword.  For example:

.. code-block:: c++

  // Avoid if `Example` is defined as a struct.
  class Example;

  // OK.
  struct Example;

  struct Example { ... };
-->

- 宣言と定義では、同じキーワードを使う必要があります。`class`での宣言に対しては`class`での定義が必要です。`struct`でも同様です。

```cpp:例
// Avoid if `Example` is defined as a struct.
class Example;

// OK.
struct Example;

struct Example { ... };
```

<!--
* ``struct`` should be used when *all* members are declared public.

.. code-block:: c++

  // Avoid using `struct` here, use `class` instead.
  struct Foo {
  private:
    int Data;
  public:
    Foo() : Data(0) { }
    int getData() const { return Data; }
    void setData(int D) { Data = D; }
  };

  // OK to use `struct`: all members are public.
  struct Bar {
    int Data;
    Bar() : Data(0) { }
  };
-->

- *すべての*メンバーがpublic宣言されている場合には`struct`を用いるべきです。

```cpp
// Avoid using `struct` here, use `class` instead.
struct Foo {
private:
  int Data;
public:
  Foo() : Data(0) { }
  int getData() const { return Data; }
  void setData(int D) { Data = D; }
};

// OK to use `struct`: all members are public.
struct Bar {
  int Data;
  Bar() : Data(0) { }
};
```

<!--
Do not use Braced Initializer Lists to Call a Constructor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting from C++11 there is a "generalized initialization syntax" which allows
calling constructors using braced initializer lists. Do not use these to call
constructors with non-trivial logic or if you care that you're calling some
*particular* constructor. Those should look like function calls using
parentheses rather than like aggregate initialization. Similarly, if you need
to explicitly name the type and call its constructor to create a temporary,
don't use a braced initializer list. Instead, use a braced initializer list
(without any type for temporaries) when doing aggregate initialization or
something notionally equivalent.
-->

#### ブレース初期化子リストはコンストラクタ呼び出しに使わない

C++11以降では「一般初期化構文（generalized initialization syntax）」があり、ブレース初期化子リストを使ってコンストラクタを呼べます。重要なロジックや*特定の*コンストラクタを呼び出したい場合、これらを使わないでください。それらは集約初期化というよりも括弧を使った関数呼び出しでしょう。同様に、名前の付いた型をその場で生成するためにコンストラクタを呼ぶ場合、ブレース初期化子リストを使わないでください。代わりに、集約等ではブレース初期化リスト（一時的な型を除く）を使います。

<!--
Examples:

.. code-block:: c++

  class Foo {
  public:
    // Construct a Foo by reading data from the disk in the whizbang format, ...
    Foo(std::string filename);

    // Construct a Foo by looking up the Nth element of some global data ...
    Foo(int N);

    // ...
  };

  // The Foo constructor call is reading a file, don't use braces to call it.
  std::fill(foo.begin(), foo.end(), Foo("name"));

  // The pair is being constructed like an aggregate, use braces.
  bar_map.insert({my_key, my_value});

If you use a braced initializer list when initializing a variable, use an equals before the open curly brace:

.. code-block:: c++

  int data[] = {0, 1, 2, 3};
-->

```cpp:例
class Foo {
public:
  // Construct a Foo by reading data from the disk in the whizbang format, ...
  Foo(std::string filename);

  // Construct a Foo by looking up the Nth element of some global data ...
  Foo(int N);

  // ...
};

// The Foo constructor call is reading a file, don't use braces to call it.
std::fill(foo.begin(), foo.end(), Foo("name"));

// The pair is being constructed like an aggregate, use braces.
bar_map.insert({my_key, my_value});
```

変数の初期化でブレース初期化子リストを使う場合は、等号を使います。

```cpp
  int data[] = {0, 1, 2, 3};
```

<!--
Use ``auto`` Type Deduction to Make Code More Readable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some are advocating a policy of "almost always ``auto``" in C++11, however LLVM
uses a more moderate stance. Use ``auto`` if and only if it makes the code more
readable or easier to maintain. Don't "almost always" use ``auto``, but do use
``auto`` with initializers like ``cast<Foo>(...)`` or other places where the
type is already obvious from the context. Another time when ``auto`` works well
for these purposes is when the type would have been abstracted away anyways,
often behind a container's typedef such as ``std::vector<T>::iterator``.

Similarly, C++14 adds generic lambda expressions where parameter types can be
``auto``. Use these where you would have used a template.
-->

#### コードを読みやすくするために`auto`型推論を使う

C++11では「たいてい`auto`」という主張もありますが、LLVMはより緩やかなスタンスを使用しています。コードの可読性や保守性が上がる場合のみ`auto`を使ってください。`auto`を使うのに「たいてい」とはしませんが、`cast<Foo>(...)`等の初期化や、ほかの場所でも文脈から明らかな場合は`auto`を使ってください。また、抽象化されすぎている型に対しても`auto`は有用です。`std::vector<T>::iterator`のようなコンテナクラス内の型定義は抽象化されすぎている型の典型例でしょう。

同様に、C++14はパラメータの型が`auto`になるジェネリックラムダ式を追加します。テンプレートを使っていたところでこれらを使います。

<!--
Beware unnecessary copies with ``auto``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The convenience of ``auto`` makes it easy to forget that its default behavior
is a copy.  Particularly in range-based ``for`` loops, careless copies are
expensive.

Use ``auto &`` for values and ``auto *`` for pointers unless you need to make a
copy.
.. code-block:: c++

  // Typically there's no reason to copy.
  for (const auto &Val : Container) observe(Val);
  for (auto &Val : Container) Val.change();

  // Remove the reference if you really want a new copy.
  for (auto Val : Container) { Val.change(); saveSomewhere(Val); }

  // Copy pointers, but make it clear that they're pointers.
  for (const auto *Ptr : Container) observe(*Ptr);
  for (auto *Ptr : Container) Ptr->change();
-->

#### `auto`での不必要なコピーに注意

`auto`の利便性は、そのデフォルト動作がコピーであることをよく忘れさせます。特に範囲ベース`for`ループでは、不注意なコピーが高くつきます。

結果のコピーが不要であれば、値には`auto &`を、ポインタには`auto *`を使います。

```cpp
// Typically there's no reason to copy.
for (const auto &Val : Container) observe(Val);
for (auto &Val : Container) Val.change();

// Remove the reference if you really want a new copy.
for (auto Val : Container) { Val.change(); saveSomewhere(Val); }

// Copy pointers, but make it clear that they're pointers.
for (const auto *Ptr : Container) observe(*Ptr);
for (auto *Ptr : Container) Ptr->change();
```

<!--
Beware of non-determinism due to ordering of pointers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In general, there is no relative ordering among pointers. As a result,
when unordered containers like sets and maps are used with pointer keys
the iteration order is undefined. Hence, iterating such containers may
result in non-deterministic code generation. While the generated code
might work correctly, non-determinism can make it harder to reproduce bugs and
debug the compiler.

In case an ordered result is expected, remember to
sort an unordered container before iteration. Or use ordered containers
like ``vector``/``MapVector``/``SetVector`` if you want to iterate pointer
keys.
-->

#### ポインタ順序による非決定性に注意

一般に、ポインタ間で順序はありません。その結果、setやmapのように順序のないコンテナで、キーにポインタが使われる場合、反復（iteration）順序は未定義です。したがって、そのようなコンテナの反復は結果として非決定的[^nondeterministic]なコードが生成されます。生成されたコードは正しく動く可能性がありますが、非決定性により再現しないバグを生じデバッグが難しくなる恐れもあります。

[^nondeterministic]: 訳注：実行毎に順序が変わりうる。

順序ある結果を期待する場合は、順序なしコンテナの反復前にソートしてください。それか、ポインタキーを反復したいなら``vector``/``MapVector``/``SetVector``のような順序付きコンテナを使います。

<!--
Beware of non-deterministic sorting order of equal elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``std::sort`` uses a non-stable sorting algorithm in which the order of equal
elements is not guaranteed to be preserved. Thus using ``std::sort`` for a
container having equal elements may result in non-deterministic behavior.
To uncover such instances of non-determinism, LLVM has introduced a new
llvm::sort wrapper function. For an EXPENSIVE_CHECKS build this will randomly
shuffle the container before sorting. Default to using ``llvm::sort`` instead
of ``std::sort``.
-->

#### 等しい要素のソートによる非決定性に注意

`std::sort`は安定ソートではありません。そのため、等しい要素を持つコンテナに`std::sort`を使うと、非決定的な動作となる恐れがあります。
この非決定的な挙動を見つけるため、LLVMは新しいllvm::sortラッパ関数を導入しました。EXPENSIVE_CHECKSビルドの場合、ソート前にコンテナをランダムにシャッフルします。`std::sort`ではなく`llvm::sort`をデフォルトで使います。

<!--
Style Issues
============

The High-Level Issues
---------------------
-->

## スタイルの問題

### 高位の問題

<!--
Self-contained Headers
^^^^^^^^^^^^^^^^^^^^^^

Header files should be self-contained (compile on their own) and end in ``.h``.
Non-header files that are meant for inclusion should end in ``.inc`` and be
used sparingly.

All header files should be self-contained. Users and refactoring tools should
not have to adhere to special conditions to include the header. Specifically, a
header should have header guards and include all other headers it needs.

There are rare cases where a file designed to be included is not
self-contained. These are typically intended to be included at unusual
locations, such as the middle of another file. They might not use header
guards, and might not include their prerequisites. Name such files with the
.inc extension. Use sparingly, and prefer self-contained headers when possible.

In general, a header should be implemented by one or more ``.cpp`` files.  Each
of these ``.cpp`` files should include the header that defines their interface
first.  This ensures that all of the dependences of the header have been
properly added to the header itself, and are not implicit.  System headers
should be included after user headers for a translation unit.
-->

#### 自己完結型ヘッダ

ヘッダファイルは自己完結型（それのみでコンパイル）とし、`.h`で終えます。
読み込みを意図した非ヘッダファイルは`.inc`で終え、注意して使ってください。

すべてのヘッダは自己完結型にします。ユーザーとリファクタリングツールはincludeのために特別な条件に従う必要はありません。具体的には、ヘッダはインクルードガードを持ち、必要なすべてのヘッダをincludeします。

まれな例として、読み込みを意図したファイルは自己完結型ではありません。これらは通常、別のファイルの途中などでincludeされます。インクルードガードを使わなかったり、前提条件を含まない可能性があります。そのようなファイルには「.inc」拡張子を付けてください。控えめ使い、できるだけ自己完結型ヘッダファイルを優先してください。

一般的に、ヘッダは1つ以上の`.cpp`ファイルで実装されます。これらの`.cpp`ファイルは、始めにインタフェースを定義したヘッダをincludeします。これにより依存関係すべてが暗黙なく適切にヘッダに含まれることが保証されます。システムヘッダは翻訳単位のユーザーヘッダの後にincludeします。

<!--
Library Layering
^^^^^^^^^^^^^^^^

A directory of header files (for example ``include/llvm/Foo``) defines a
library (``Foo``). One library (both
its headers and implementation) should only use things from the libraries
listed in its dependencies.

Some of this constraint can be enforced by classic Unix linkers (Mac & Windows
linkers, as well as lld, do not enforce this constraint). A Unix linker
searches left to right through the libraries specified on its command line and
never revisits a library. In this way, no circular dependencies between
libraries can exist.

This doesn't fully enforce all inter-library dependencies, and importantly
doesn't enforce header file circular dependencies created by inline functions.
A good way to answer the "is this layered correctly" would be to consider
whether a Unix linker would succeed at linking the program if all inline
functions were defined out-of-line. (& for all valid orderings of dependencies
- since linking resolution is linear, it's possible that some implicit
dependencies can sneak through: A depends on B and C, so valid orderings are
"C B A" or "B C A", in both cases the explicit dependencies come before their
use. But in the first case, B could still link successfully if it implicitly
depended on C, or the opposite in the second case)
-->

#### ライブラリの階層化

ヘッダファイルのディレクトリ（たとえば`include/llvm/Foo`）はライブラリ（`Foo`）を定義します。あるライブラリ（ヘッダおよび実装）では依存関係リストにあるライブラリのもののみが使えます。

この制約が適用できるのは旧来のUnixリンカです（Mac & Windowsのリンカはlldと同様にこの制約を適用しません）。Unixリンカはコマンドラインで指定されたライブラリを左から右に検索します。ライブラリの循環依存は存在できません。

これはすべてのライブラリ間の依存を完全に強制するわけではありません。また重要なこととして、インライン関数によるヘッダファイルの循環依存は強制しません。
「これが正しく階層化されているか」に答える良い方法は、すべてのインライン関数がout-of-lineで定義された場合でもUnixリンカが成功するか考えてみることです。
（さらに依存関係の有効な順序すべてについて。リンク解決は線形のため、いくつかの暗黙の依存関係についてすり抜ける恐れがあります。AはBとCに依存するので、有効な順序は「C B A」や「B C A」です。どちらも利用の前に明示的な依存が来ます。ただし前者では暗黙的にBがCに依存している場合リンクが成功し、後者はその逆です）

<!--
.. _minimal list of #includes:

``#include`` as Little as Possible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``#include`` hurts compile time performance.  Don't do it unless you have to,
especially in header files.

But wait! Sometimes you need to have the definition of a class to use it, or to
inherit from it.  In these cases go ahead and ``#include`` that header file.  Be
aware however that there are many cases where you don't need to have the full
definition of a class.  If you are using a pointer or reference to a class, you
don't need the header file.  If you are simply returning a class instance from a
prototyped function or method, you don't need it.  In fact, for most cases, you
simply don't need the definition of a class. And not ``#include``\ing speeds up
compilation.

It is easy to try to go too overboard on this recommendation, however.  You
**must** include all of the header files that you are using --- you can include
them either directly or indirectly through another header file.  To make sure
that you don't accidentally forget to include a header file in your module
header, make sure to include your module header **first** in the implementation
file (as mentioned above).  This way there won't be any hidden dependencies that
you'll find out about later.
-->

#### `#include`は最低限に

`#include`はコンパイル時間を損ないます。どうしても必要でない場合は行わないでください、特にヘッダファイルでは。

でもちょっと待って！　使ったり、継承したりするためにクラス定義が必要になることがあります。その場合はどうぞ`#include`してください。ですが、クラスの完全な定義が必要でない場合も多いことに注意してください。以下の場合、ヘッダファイルは不要です。

- クラスのポインタや参照を使うだけの場合
- 関数やメソッド宣言の戻り値で使うだけ（ヘッダにその関数定義を含まない）の場合

この勧めをやりすぎるのは簡単ですが、使っているヘッダファイルのすべてがインクルードされなくては**なりません**。直接または別のヘッダファイルを介して間接的にそれらをインクルードできます。モジュールヘッダ内でのインクルード漏れを確認する方法があります。前述のように実装ファイルの**最初に**モジュールヘッダを含めるようにしてください。この方法により、隠れた依存関係がコンパイルエラーとなり発覚します。

<!--
Keep "Internal" Headers Private
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Many modules have a complex implementation that causes them to use more than one
implementation (``.cpp``) file.  It is often tempting to put the internal
communication interface (helper classes, extra functions, etc) in the public
module header file.  Don't do this!

If you really need to do something like this, put a private header file in the
same directory as the source files, and include it locally.  This ensures that
your private interface remains private and undisturbed by outsiders.

.. note::

    It's okay to put extra implementation methods in a public class itself. Just
    make them private (or protected) and all is well.
-->

#### 「内部」ヘッダは非公開

多くのモジュールは、複数の実装（`.cpp`）ファイルを使うことで複雑な実装を持っています。多くの場合、内部通信インタフェース（ヘルパークラス、余分な機能など）を公開モジュールヘッダファイルに置くことは魅力的です。でもやめて！

本当に必要な場合は、ソースファイルと同じディレクトリに非公開ヘッダファイルを置いて、それを内々でインクルードしてください。これは、非公開インタフェースが他者に乱されず非公開であることを保証します。

:::note
publicクラス自体に追加の実装メソッドを入れてもかまいません。private（またはprotected）とすることで、うまくいきます。
:::

<!--
Use Namespace Qualifiers to Implement Previously Declared Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->

#### 宣言された関数の実装には名前空間修飾子を用いる

<!--
When providing an out of line implementation of a function in a source file, do
not open namespace blocks in the source file. Instead, use namespace qualifiers
to help ensure that your definition matches an existing declaration. Do this:

.. code-block:: c++

  // Foo.h
  namespace llvm {
  int foo(const char *s);
  }

  // Foo.cpp
  #include "Foo.h"
  using namespace llvm;
  int llvm::foo(const char *s) {
    // ...
  }
-->

ソースファイルで関数のアウトオブラインを実装する場合は、ソースファイルで名前空間ブロックを開かないでください。代わりに、名前空間修飾子を使い定義が既存の宣言と一致するようにします。次のようにします。

```cpp
// Foo.h
namespace llvm {
int foo(const char *s);
}

// Foo.cpp
#include "Foo.h"
using namespace llvm;
int llvm::foo(const char *s) {
  // ...
}
```

<!--
Doing this helps to avoid bugs where the definition does not match the
declaration from the header. For example, the following C++ code defines a new
overload of ``llvm::foo`` instead of providing a definition for the existing
function declared in the header:

.. code-block:: c++

  // Foo.cpp
  #include "Foo.h"
  namespace llvm {
  int foo(char *s) { // Mismatch between "const char *" and "char *"
  }
  } // namespace llvm
-->

こうすることで定義がヘッダでの宣言と一致しないというバグを避けやすくなります。たとえば、次のC++コードは``llvm::foo``についてヘッダで宣言された既存の関数の定義ではなく新たなオーバーロードを定義してしまいます。

```cpp
// Foo.cpp
#include "Foo.h"
namespace llvm {
int foo(char *s) { // Mismatch between "const char *" and "char *"
}
} // namespace llvm
```

<!--
This error will not be caught until the build is nearly complete, when the
linker fails to find a definition for any uses of the original function.  If the
function were instead defined with a namespace qualifier, the error would have
been caught immediately when the definition was compiled.

Class method implementations must already name the class and new overloads
cannot be introduced out of line, so this recommendation does not apply to them.
-->

このエラーはリンカが元の関数を使うための定義を探せない時、つまりビルドがほぼ終わるまで検出されません。もしこの関数が名前空間修飾子で定義されていれば、コンパイル時点で検出されたでしょう。

クラスメソッドは実装にそのクラス名をつける必要があること、アウトオブラインでオーバーロードできないことから、この勧告の適用外です。

<!--
.. _early exits:
Use Early Exits and ``continue`` to Simplify Code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When reading code, keep in mind how much state and how many previous decisions
have to be remembered by the reader to understand a block of code.  Aim to
reduce indentation where possible when it doesn't make it more difficult to
understand the code.  One great way to do this is by making use of early exits
and the ``continue`` keyword in long loops. Consider this code that does not
use an early exit:

.. code-block:: c++

  Value *doSomething(Instruction *I) {
    if (!I->isTerminator() &&
        I->hasOneUse() && doOtherThing(I)) {
      ... some long code ....
    }

    return 0;
  }
-->

#### 早期終了と`continue`でコードをシンプルに

なるべくインデントを減らすことは、コードを理解しやすくします。1つの方法は、早期終了する（Early Exits）ことと、長いループで`continue`キーワードを使うことです。早期終了を使わない次のコードを考えてみます。

```cpp:悪い例
Value *doSomething(Instruction *I) {
  if (!I->isTerminator() &&
      I->hasOneUse() && doOtherThing(I)) {
    ... some long code ....
  }

  return 0;
}
```

<!--
This code has several problems if the body of the ``'if'`` is large.  When
you're looking at the top of the function, it isn't immediately clear that this
*only* does interesting things with non-terminator instructions, and only
applies to things with the other predicates.  Second, it is relatively difficult
to describe (in comments) why these predicates are important because the ``if``
statement makes it difficult to lay out the comments.  Third, when you're deep
within the body of the code, it is indented an extra level.  Finally, when
reading the top of the function, it isn't clear what the result is if the
predicate isn't true; you have to read to the end of the function to know that
it returns null.
-->

`'if'`の本文が大きい場合、このコードにはいくつか問題があります。第一に、関数の先頭を見ただけでは、条件に合わない場合何もしないことが分かりません。第二に、`if`文はコメントしづらいレイアウトのため、なぜそれら述部が重要であるかコメントすることは割合難しいです。第三に、コード本体の深いところでは、余分にインデントされます。最後に、関数の先頭を見ただけでは条件に合わない場合、戻り値が何であるかは明らかではありません。nullを返すことを知るためには、関数の最後まで読まなければなりません。

<!--
It is much preferred to format the code like this:

.. code-block:: c++

  Value *doSomething(Instruction *I) {
    // Terminators never need 'something' done to them because ...
    if (I->isTerminator())
      return 0;

    // We conservatively avoid transforming instructions with multiple uses
    // because goats like cheese.
    if (!I->hasOneUse())
      return 0;

    // This is really just here for example.
    if (!doOtherThing(I))
      return 0;

    ... some long code ....
  }
-->

```cpp:良い例
Value *doSomething(Instruction *I) {
  // Terminators never need 'something' done to them because ...
  if (I->isTerminator())
    return 0;

  // We conservatively avoid transforming instructions with multiple uses
  // because goats like cheese.
  if (!I->hasOneUse())
    return 0;

  // This is really just here for example.
  if (!doOtherThing(I))
    return 0;

  ... some long code ....
}
```

<!--
This fixes these problems.  A similar problem frequently happens in ``for``
loops.  A silly example is something like this:

.. code-block:: c++

  for (Instruction &I : BB) {
    if (auto *BO = dyn_cast<BinaryOperator>(&I)) {
      Value *LHS = BO->getOperand(0);
      Value *RHS = BO->getOperand(1);
      if (LHS != RHS) {
        ...
      }
    }
  }
-->

同様の問題は`for`ループで頻繁に起きます。愚かな例を示します。

```cpp:愚かな例
for (Instruction &I : BB) {
  if (auto *BO = dyn_cast<BinaryOperator>(&I)) {
    Value *LHS = BO->getOperand(0);
    Value *RHS = BO->getOperand(1);
    if (LHS != RHS) {
      ...
    }
  }
}
```

<!--
When you have very, very small loops, this sort of structure is fine. But if it
exceeds more than 10-15 lines, it becomes difficult for people to read and
understand at a glance. The problem with this sort of code is that it gets very
nested very quickly. Meaning that the reader of the code has to keep a lot of
context in their brain to remember what is going immediately on in the loop,
because they don't know if/when the ``if`` conditions will have ``else``\s etc.
It is strongly preferred to structure the loop like this:

.. code-block:: c++

  for (Instruction &I : BB) {
    auto *BO = dyn_cast<BinaryOperator>(&I);
    if (!BO) continue;

    Value *LHS = BO->getOperand(0);
    Value *RHS = BO->getOperand(1);
    if (LHS == RHS) continue;

    ...
  }
-->

非常に小さなループでは、この構造の問題はありません。10〜15行を超えた場合、一目で理解することは困難になります。この種のコードの問題は、あっという間にネストされてしまうことです。それはコードの読み手は、ループ内で何が行われているか把握するために、非常に多くのコンテキストを覚えておかなくてはならないことを意味します。なぜなら、彼らは`if`条件に`else`等があるかどうかを知りません。次のようなループを構成することが望ましいです。

```cpp:良い例
for (Instruction &I : BB) {
  auto *BO = dyn_cast<BinaryOperator>(&I);
  if (!BO) continue;

  Value *LHS = BO->getOperand(0);
  Value *RHS = BO->getOperand(1);
  if (LHS == RHS) continue;

  ...
}
```

<!--
This has all the benefits of using early exits for functions: it reduces nesting
of the loop, it makes it easier to describe why the conditions are true, and it
makes it obvious to the reader that there is no ``else`` coming up that they
have to push context into their brain for.  If a loop is large, this can be a
big understandability win.
-->

これには、関数の早期終了を使う利点がすべて備わっています。ループのネストを減らし、条件に該当する理由を簡単に記述でき、そして`else`を気にしなくてよいことが明らかです。ループが大きい場合、非常に分かりやすくなります。

<!--
Don't use ``else`` after a ``return``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For similar reasons as above (reduction of indentation and easier reading), please
do not use ``'else'`` or ``'else if'`` after something that interrupts control
flow --- like ``return``, ``break``, ``continue``, ``goto``, etc. For example:

.. code-block:: c++

  case 'J': {
    if (Signed) {
      Type = Context.getsigjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_sigjmp_buf;
        return QualType();
      } else {
        break; // Unnecessary.
      }
    } else {
      Type = Context.getjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_jmp_buf;
        return QualType();
      } else {
        break; // Unnecessary.
      }
    }
  }
-->

#### `return`後に`else`を使用しない

上記と同様の理由（インデントの減少と読みやすさ）から、制御フローの中断後に`else`や`else if`を使わないでください。制御フローの中断とは`return`、`break`、`continue`、`goto`等です。

```cpp:例
case 'J': {
  if (Signed) {
    Type = Context.getsigjmp_bufType();
    if (Type.isNull()) {
      Error = ASTContext::GE_Missing_sigjmp_buf;
      return QualType();
    } else {
      break; // Unnecessary.
    }
  } else {
    Type = Context.getjmp_bufType();
    if (Type.isNull()) {
      Error = ASTContext::GE_Missing_jmp_buf;
      return QualType();
    } else {
      break; // Unnecessary.
    }
  }
}
```

<!--
It is better to write it like this:

.. code-block:: c++

  case 'J':
    if (Signed) {
      Type = Context.getsigjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_sigjmp_buf;
        return QualType();
      }
    } else {
      Type = Context.getjmp_bufType();
      if (Type.isNull()) {
        Error = ASTContext::GE_Missing_jmp_buf;
        return QualType();
      }
    }
    break;
-->

次のように書く方が良いです。

```cpp:好ましい例
case 'J':
  if (Signed) {
    Type = Context.getsigjmp_bufType();
    if (Type.isNull()) {
      Error = ASTContext::GE_Missing_sigjmp_buf;
      return QualType();
    }
  } else {
    Type = Context.getjmp_bufType();
    if (Type.isNull()) {
      Error = ASTContext::GE_Missing_jmp_buf;
      return QualType();
    }
  }
  break;
```

<!--
Or better yet (in this case) as:

.. code-block:: c++

  case 'J':
    if (Signed)
      Type = Context.getsigjmp_bufType();
    else
      Type = Context.getjmp_bufType();

    if (Type.isNull()) {
      Error = Signed ? ASTContext::GE_Missing_sigjmp_buf :
                       ASTContext::GE_Missing_jmp_buf;
      return QualType();
    }
    break;

The idea is to reduce indentation and the amount of code you have to keep track
of when reading the code.
-->

またはいっそのこと。

```cpp:思い切った例
case 'J':
  if (Signed)
    Type = Context.getsigjmp_bufType();
  else
    Type = Context.getjmp_bufType();

  if (Type.isNull()) {
    Error = Signed ? ASTContext::GE_Missing_sigjmp_buf :
                     ASTContext::GE_Missing_jmp_buf;
    return QualType();
  }
  break;
```

この案はインデントと、コードを読み取るときに覚えておかなくてはならないコードの量を減らします。

<!--
Turn Predicate Loops into Predicate Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is very common to write small loops that just compute a boolean value.  There
are a number of ways that people commonly write these, but an example of this
sort of thing is:

.. code-block:: c++

  bool FoundFoo = false;
  for (unsigned I = 0, E = BarList.size(); I != E; ++I)
    if (BarList[I]->isFoo()) {
      FoundFoo = true;
      break;
    }

  if (FoundFoo) {
    ...
  }
-->

#### Predicateはループから関数へ

成否判定だけの小さなループを書くことは非常に一般的です。これを書く方法は各種ありますが、たとえば次のようなものです。

```cpp:例
bool FoundFoo = false;
for (unsigned I = 0, E = BarList.size(); I != E; ++I)
  if (BarList[I]->isFoo()) {
    FoundFoo = true;
    break;
  }

if (FoundFoo) {
  ...
}
```

<!--
Instead of this sort of loop, we prefer to use a predicate function (which may
be `static`_) that uses `early exits`_:

.. code-block:: c++

  /// \returns true if the specified list has an element that is a foo.
  static bool containsFoo(const std::vector<Bar*> &List) {
    for (unsigned I = 0, E = List.size(); I != E; ++I)
      if (List[I]->isFoo())
        return true;
    return false;
  }
  ...

  if (containsFoo(BarList)) {
    ...
  }
-->

この種のループの代わりに、[早期終了](#早期終了とcontinueでコードをシンプルに)するpredicate関数（[static](#無名名前空間)の場合もあります）を使いましょう。

```cpp:好ましい例
/// \returns true if the specified list has an element that is a foo.
static bool containsFoo(const std::vector<Bar*> &List) {
  for (unsigned I = 0, E = List.size(); I != E; ++I)
    if (List[I]->isFoo())
      return true;
  return false;
}
...

if (containsFoo(BarList)) {
  ...
}
```

<!--
There are many reasons for doing this: it reduces indentation and factors out
code which can often be shared by other code that checks for the same predicate.
More importantly, it *forces you to pick a name* for the function, and forces
you to write a comment for it.  In this silly example, this doesn't add much
value.  However, if the condition is complex, this can make it a lot easier for
the reader to understand the code that queries for this predicate.  Instead of
being faced with the in-line details of how we check to see if the BarList
contains a foo, we can trust the function name and continue reading with better
locality.
-->

これを行うには多くの理由があります。インデントを減らし、しばしば共有できる同じチェックを行う別のコードとの重複を排除します。さらに重要なのは、関数の*命名を強制*し、それにコメントを書くことを強制します。このちっぽけな例では、大した価値がありません。ですが条件が複雑な場合は、predicateクエリをより簡単に理解できるようになるでしょう。インラインで詳細にBarListがfooを含むかをどのようにチェックするのかについて直面するのではなく、関数名を信頼しより良い局所性で読んでいけます。

<!--

The Low-Level Issues
--------------------

Name Types, Functions, Variables, and Enumerators Properly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Poorly-chosen names can mislead the reader and cause bugs. We cannot stress
enough how important it is to use *descriptive* names.  Pick names that match
the semantics and role of the underlying entities, within reason.  Avoid
abbreviations unless they are well known.  After picking a good name, make sure
to use consistent capitalization for the name, as inconsistency requires clients
to either memorize the APIs or to look it up to find the exact spelling.
In general, names should be in camel case (e.g. ``TextFileReader`` and
``isLValue()``).  Different kinds of declarations have different rules:
-->

### 低位の問題

#### 型、関数、変数、および列挙子への適切な命名

下手に選ばれた名前は、読者に誤解を与え、バグを引き起こす可能性があります。私たちは、*わかりやすい*名前を使うことがどれだけ重要か、とても十分に強調しきれません。常識の範囲で、要素の意味と役割に一致する名前を選んでください。よく知られていない限り略語は避けてください。良い名前を選んだ後、名前に一貫した大文字を使ってください。ブレがあると、利用者はいちいち細かいスペルに煩わされます。

一般に、名前はキャメルケース（例：`TextFileReader`と`isLValue()`）でなければなりません。種類ごとにルールがあります。

<!--
* **Type names** (including classes, structs, enums, typedefs, etc) should be
  nouns and start with an upper-case letter (e.g. ``TextFileReader``).

* **Variable names** should be nouns (as they represent state).  The name should
  be camel case, and start with an upper case letter (e.g. ``Leader`` or
  ``Boats``).

* **Function names** should be verb phrases (as they represent actions), and
  command-like function should be imperative.  The name should be camel case,
  and start with a lower case letter (e.g. ``openFile()`` or ``isFoo()``).

* **Enum declarations** (e.g. ``enum Foo {...}``) are types, so they should
  follow the naming conventions for types.  A common use for enums is as a
  discriminator for a union, or an indicator of a subclass.  When an enum is
  used for something like this, it should have a ``Kind`` suffix
  (e.g. ``ValueKind``).

* **Enumerators** (e.g. ``enum { Foo, Bar }``) and **public member variables**
  should start with an upper-case letter, just like types.  Unless the
  enumerators are defined in their own small namespace or inside a class,
  enumerators should have a prefix corresponding to the enum declaration name.
  For example, ``enum ValueKind { ... };`` may contain enumerators like
  ``VK_Argument``, ``VK_BasicBlock``, etc.  Enumerators that are just
  convenience constants are exempt from the requirement for a prefix.  For
  instance:

  .. code-block:: c++

      enum {
        MaxSize = 42,
        Density = 12
      };
-->

- **型名**（クラス、構造体、列挙型、typedef等を含む）は、名詞かつ大文字で始めます（例：`TextFileReader`）。
- **変数名**は（状態を代表するような）名詞とします。名前はキャメルケースで、大文字で始めます（例：`Leader`や`Boats`）。
- **関数名**は（アクション表すような）動詞であるべきで、コマンドのような関数は命令型とします。名前はキャメルケースで、小文字で始めます（例：`openFile()`や`isFoo()`）。
- **列挙型宣言**（例： `enum Foo {...}`）は型のため、型名の規則に準じます。列挙型は一般に、共用体（union）の弁別や、サブクラスの情報提供のために使います。列挙型は、このような何かのために使われる場合、`Kind`で終わります（例：`ValueKind`）。
- **列挙子**（例：`enum { Foo, Bar }`）と**パブリックメンバー変数**は、型と同様に大文字で始めます。列挙子は、小さな名前空間内やクラス内で定義されていない限り、列挙型の宣言名に対応する接頭辞を持ちます。たとえば、`enum ValueKind { ...};`は`VK_Argument`、`VK_BasicBlock`といったような列挙子を含むでしょう。便利な定数としての列挙子は、接頭辞の要件が免除されます。

```cpp:定数列挙子の例
enum {
  MaxSize = 42,
  Density = 12
};
```

<!--
As an exception, classes that mimic STL classes can have member names in STL's
style of lower-case words separated by underscores (e.g. ``begin()``,
``push_back()``, and ``empty()``). Classes that provide multiple
iterators should add a singular prefix to ``begin()`` and ``end()``
(e.g. ``global_begin()`` and ``use_begin()``).

Here are some examples:

.. code-block:: c++

  class VehicleMaker {
    ...
    Factory<Tire> F;            // Avoid: a non-descriptive abbreviation.
    Factory<Tire> Factory;      // Better: more descriptive.
    Factory<Tire> TireFactory;  // Even better: if VehicleMaker has more than one
                                // kind of factories.
  };

  Vehicle makeVehicle(VehicleType Type) {
    VehicleMaker M;                         // Might be OK if scope is small.
    Tire Tmp1 = M.makeTire();               // Avoid: 'Tmp1' provides no information.
    Light Headlight = M.makeLight("head");  // Good: descriptive.
    ...
  }
-->

例外として、STLクラスを模倣するクラスがあります。このクラスは、アンダースコアで区切られた小文字の単語というSTLのスタイルでメンバー名を持てます（例：`begin()`、`push_back()`と`empty()`）。複数のイテレータを提供するクラスは`begin()`と`end()`に特異な接頭辞を追加する必要があります（例：`global_begin()`と `use_begin()`）。

```cpp:例
class VehicleMaker {
  ...
  Factory<Tire> F;            // Avoid: a non-descriptive abbreviation.
  Factory<Tire> Factory;      // Better: more descriptive.
  Factory<Tire> TireFactory;  // Even better: if VehicleMaker has more than one
                              // kind of factories.
};

Vehicle makeVehicle(VehicleType Type) {
  VehicleMaker M;                         // Might be OK if scope is small.
  Tire Tmp1 = M.makeTire();               // Avoid: 'Tmp1' provides no information.
  Light Headlight = M.makeLight("head");  // Good: descriptive.
  ...
}
```

<!--
Assert Liberally
^^^^^^^^^^^^^^^^

Use the "``assert``" macro to its fullest.  Check all of your preconditions and
assumptions, you never know when a bug (not necessarily even yours) might be
caught early by an assertion, which reduces debugging time dramatically.  The
"``<cassert>``" header file is probably already included by the header files you
are using, so it doesn't cost anything to use it.

To further assist with debugging, make sure to put some kind of error message in
the assertion statement, which is printed if the assertion is tripped. This
helps the poor debugger make sense of why an assertion is being made and
enforced, and hopefully what to do about it.  Here is one complete example:

.. code-block:: c++

  inline Value *getOperand(unsigned I) {
    assert(I < Operands.size() && "getOperand() out of range!");
    return Operands[I];
  }
-->

#### たっぷりのアサート

「`assert`」マクロを最大限に使います。すべての前提条件と仮定をチェックすれば、バグ（あなたのものとは限りません）がアサーションによって早く発見できるとは限りませんが、デバッグ時間は劇的に減ります。「`<cassert>`」ヘッダファイルは、おそらくもうインクルードされているので、追加のコストはかからないでしょう。

さらに、デバッグを支援するために、アサーション文に何らかのエラーメッセージを入れてください。これは、アサーションの発生原因とそれについて何をすべきかを、未熟なデバッガが理解する助けとなります。

```cpp:一つの完全な例
inline Value *getOperand(unsigned I) {
  assert(I < Operands.size() && "getOperand() out of range!");
  return Operands[I];
}
```

<!--
Here are more examples:

.. code-block:: c++

  assert(Ty->isPointerType() && "Can't allocate a non-pointer type!");

  assert((Opcode == Shl || Opcode == Shr) && "ShiftInst Opcode invalid!");

  assert(idx < getNumSuccessors() && "Successor # out of range!");

  assert(V1.getType() == V2.getType() && "Constant types must be identical!");

  assert(isa<PHINode>(Succ->front()) && "Only works on PHId BBs!");
-->

```cpp:多くの例
assert(Ty->isPointerType() && "Can't allocate a non-pointer type!");
assert((Opcode == Shl || Opcode == Shr) && "ShiftInst Opcode invalid!");
assert(idx < getNumSuccessors() && "Successor # out of range!");
assert(V1.getType() == V2.getType() && "Constant types must be identical!");
assert(isa<PHINode>(Succ->front()) && "Only works on PHId BBs!");
```

<!--
You get the idea.

In the past, asserts were used to indicate a piece of code that should not be
reached.  These were typically of the form:

.. code-block:: c++

  assert(0 && "Invalid radix for integer literal");

This has a few issues, the main one being that some compilers might not
understand the assertion, or warn about a missing return in builds where
assertions are compiled out.

Today, we have something much better: ``llvm_unreachable``:

.. code-block:: c++

  llvm_unreachable("Invalid radix for integer literal");

When assertions are enabled, this will print the message if it's ever reached
and then exit the program. When assertions are disabled (i.e. in release
builds), ``llvm_unreachable`` becomes a hint to compilers to skip generating
code for this branch. If the compiler does not support this, it will fall back
to the "abort" implementation.
-->

過去には、コードに到達すべきではないと示すためにアサートが使われました。

```cpp:典型例
assert(0 && "Invalid radix for integer literal");
```

これにはいくつかの問題があります。主なものは、いくつかのコンパイラはアサーションを理解しない可能性があり、あるいはアサーションの部分でreturnが抜けていると警告を出すことです。

今日、私たちにはより良いものがあります。`llvm_unreachable`。

```cpp:好ましい例
llvm_unreachable("Invalid radix for integer literal");
```

アサーションを有効にすると、ここに到達した時点でメッセージを表示し、プログラムを終了します。アサーションが無効になっている場合（つまりリリースビルドでは）、`llvm_unreachable`はこの分岐のコード生成は省略可能だというコンパイラへのヒントとなります。コンパイラがこれをサポートしていない場合は、「abort」実装にフォールバックされます。

<!--
Use ``llvm_unreachable`` to mark a specific point in code that should never be
reached. This is especially desirable for addressing warnings about unreachable
branches, etc., but can be used whenever reaching a particular code path is
unconditionally a bug (not originating from user input; see below) of some kind.
Use of ``assert`` should always include a testable predicate (as opposed to
``assert(false)``).

If the error condition can be triggered by user input then the
recoverable error mechanism described in :doc:`ProgrammersManual` should be
used instead. In cases where this is not practical, ``report_fatal_error`` may
be used.
-->

``llvm_unreachable``を使い到達してはならないコードの一点にマークします。これは到達しない分岐などの警告への対処として望ましいですが、使えるのはそこへの到達が無条件に何らかのバグ（ユーザーからの入力ではなく。以下を参照）となる場合です。
``assert``の使用時は常にテスト可能なpredicate（``assert(false)``とは異なります）を含める必要があります。

ユーザーの入力によりエラー状態となりうる場合は、代わりに[LLVM Programmer's Manual](https://releases.llvm.org/14.0.0/docs/ProgrammersManual.html)で示す回復可能なエラーメカニズムを使う必要があります。それが実用的でない場合は、``report_fatal_error``も使えます。

<!--
Another issue is that values used only by assertions will produce an "unused
value" warning when assertions are disabled.  For example, this code will warn:

.. code-block:: c++

  unsigned Size = V.size();
  assert(Size > 42 && "Vector smaller than it should be");

  bool NewToSet = Myset.insert(Value);
  assert(NewToSet && "The value shouldn't be in the set yet");

These are two interesting different cases. In the first case, the call to
``V.size()`` is only useful for the assert, and we don't want it executed when
assertions are disabled.  Code like this should move the call into the assert
itself.  In the second case, the side effects of the call must happen whether
the assert is enabled or not.  In this case, the value should be cast to void to
disable the warning.  To be specific, it is preferred to write the code like
this:

.. code-block:: c++

  assert(V.size() > 42 && "Vector smaller than it should be");

  bool NewToSet = Myset.insert(Value); (void)NewToSet;
  assert(NewToSet && "The value shouldn't be in the set yet");
-->

別の問題は、アサーションが無効になっている場合に、アサーションによってのみ使用される値で「未使用値」という警告が生成されるということです。

```cpp:警告となる例
unsigned Size = V.size();
assert(Size > 42 && "Vector smaller than it should be");

bool NewToSet = Myset.insert(Value);
assert(NewToSet && "The value shouldn't be in the set yet");
```

2つの興味深い例があります。最初の例では、`V.size()`の呼び出しはアサートのためにのみ有用であり、アサーションが無効になっている場合に実行されたくありません。このようなコードは、アサート自体に呼び出しを移動する必要があります。次の例では、呼び出しの副作用はアサートが有効かどうかによらず起きなければなりません。この場合、警告を無効にするには値をvoidにキャストします。具体的には、このようなコードがよいでしょう。

```cpp:好ましい例
assert(V.size() > 42 && "Vector smaller than it should be");

bool NewToSet = Myset.insert(Value); (void)NewToSet;
assert(NewToSet && "The value shouldn't be in the set yet");
```

<!--
Do Not Use ``using namespace std``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In LLVM, we prefer to explicitly prefix all identifiers from the standard
namespace with an "``std::``" prefix, rather than rely on "``using namespace
std;``".

In header files, adding a ``'using namespace XXX'`` directive pollutes the
namespace of any source file that ``#include``\s the header, creating
maintenance issues.

In implementation files (e.g. ``.cpp`` files), the rule is more of a stylistic
rule, but is still important.  Basically, using explicit namespace prefixes
makes the code **clearer**, because it is immediately obvious what facilities
are being used and where they are coming from. And **more portable**, because
namespace clashes cannot occur between LLVM code and other namespaces.  The
portability rule is important because different standard library implementations
expose different symbols (potentially ones they shouldn't), and future revisions
to the C++ standard will add more symbols to the ``std`` namespace.  As such, we
never use ``'using namespace std;'`` in LLVM.
-->

#### `using namespace std`を使わない

LLVMでは、標準名前空間のすべての識別子について、「`using namespace std;`」に頼るのではなく、「`std::`」接頭辞を明示することを好みます。

ヘッダファイルにおいて、`'using namespace XXX'`ディレクティブの追加はそのヘッダを`#include`するソースファイルの名前空間を汚し、メンテナンスの問題が生じます。

実装ファイル（たとえば`.cpp`ファイル）では、よりスタイルの問題ですが、それでも重要です。基本的に、明示的な名前空間の接頭辞は、コードを**明解**にします。また、LLVMコードやほかの名前空間との間で名前空間の衝突が起きないため、**よりポータブル**になります。将来のC++標準の改訂では`std`名前空間へのシンボル追加もあるでしょう。ですので、私たちはLLVMで`'using namespace std;'`をけっして使いません。

<!--
The exception to the general rule (i.e. it's not an exception for the ``std``
namespace) is for implementation files.  For example, all of the code in the
LLVM project implements code that lives in the 'llvm' namespace.  As such, it is
ok, and actually clearer, for the ``.cpp`` files to have a ``'using namespace
llvm;'`` directive at the top, after the ``#include``\s.  This reduces
indentation in the body of the file for source editors that indent based on
braces, and keeps the conceptual context cleaner.  The general form of this rule
is that any ``.cpp`` file that implements code in any namespace may use that
namespace (and its parents'), but should not use any others.
-->

一般的なルールの例外（つまり、`std`名前空間の例外ではありません）は、実装ファイルのためのものです。たとえば、LLVMプロジェクト内のすべてのコードは、「llvm」名前空間内のコードを実装します。ですので、それはOKとします。実際明解ですし、`.cpp`ファイルは`#include`直後の先頭に`'using namespace llvm;'`ディレクティブがあります。これは、中括弧に基づいたインデントを行うソースエディタ向けに本文のインデントを減らし、概念的なコンテキストをきれいに保ちます。この規則を一般的に表すと、次のとおりです。

- 任意の名前空間内のコードを実装する任意の`.cpp`ファイルは、それの（そして親の）名前空間を`using`してもよい。
- 別の名前空間を`using`してはならない。

<!--
Provide a Virtual Method Anchor for Classes in Headers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a class is defined in a header file and has a vtable (either it has virtual
methods or it derives from classes with virtual methods), it must always have at
least one out-of-line virtual method in the class.  Without this, the compiler
will copy the vtable and RTTI into every ``.o`` file that ``#include``\s the
header, bloating ``.o`` file sizes and increasing link times.
-->

#### ヘッダ内クラスは仮想メソッドアンカーを提供する

クラスがヘッダファイル内で定義されvtableを持つ（仮想メソッドを持つか、そういったクラスから派生した）場合、仮想メソッドの少なくとも1つはout-of-line（.cppファイルで定義）します。これがないと、コンパイラは、そのヘッダを`#include`した`.o`ファイルすべてにvtableとRTTIをコピーし、`.o`ファイルサイズとリンク時間を増やします。これはClangの`-Wweak-vtables`警告で指摘されることがあります。

<!--
Don't use default labels in fully covered switches over enumerations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``-Wswitch`` warns if a switch, without a default label, over an enumeration
does not cover every enumeration value. If you write a default label on a fully
covered switch over an enumeration then the ``-Wswitch`` warning won't fire
when new elements are added to that enumeration. To help avoid adding these
kinds of defaults, Clang has the warning ``-Wcovered-switch-default`` which is
off by default but turned on when building LLVM with a version of Clang that
supports the warning.

A knock-on effect of this stylistic requirement is that when building LLVM with
GCC you may get warnings related to "control may reach end of non-void function"
if you return from each case of a covered switch-over-enum because GCC assumes
that the enum expression may take any representable value, not just those of
individual enumerators. To suppress this warning, use ``llvm_unreachable`` after
the switch.
-->

#### 列挙型を網羅したswitchにdefaultを使わない

`-Wswitch`は、列挙型の値を網羅せずdefaultもないswitchに警告を出します。列挙型を網羅したswitchにdefaultを書いた場合、新しい要素が列挙体に追加されても`-Wswitch`は警告しません。この種のdefaultを追加することを避けるために、Clangは`-Wcovered-switch-default`警告を持ちます。これはデフォルトで無効になっていますが、Clangの警告をサポートする版でLLVMをビルドする場合は有効になります。

この影響で、列挙型を網羅したswitchの各caseでreturnしていた場合、GCCでビルドすると「コントロールが非void型関数の終わりに到達します」関連の警告が出ます。GCCはenum句が個々の列挙子だけでなく任意の値を取れることを前提としているためです。この警告を抑止するには、switchの後に`llvm_unreachable`を使います。

<!--
Use range-based ``for`` loops wherever possible
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->

#### できるだけrange-based ``for``ループを使う

<!--
The introduction of range-based ``for`` loops in C++11 means that explicit
manipulation of iterators is rarely necessary. We use range-based ``for``
loops wherever possible for all newly added code. For example:

.. code-block:: c++

  BasicBlock *BB = ...
  for (Instruction &I : *BB)
    ... use I ...

Usage of ``std::for_each()``/``llvm::for_each()`` functions is discouraged,
unless the the callable object already exists.
-->

C++11でのrange-based ``for``ループの導入は、イテレータの明示的操作がめったにいらないことを意味します。私たちは、すべての新規追加コードに対して、できるだけrange-based ``for``ループを使います。

```cpp
BasicBlock *BB = ...
for (Instruction &I : *BB)
  ... use I ...
```

呼び出し可能なオブジェクトがない場合を除いて、``std::for_each()``/``llvm::for_each()``関数の使用はお勧めしません。

<!--
Don't evaluate ``end()`` every time through a loop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In cases where range-based ``for`` loops can't be used and it is necessary
to write an explicit iterator-based loop, pay close attention to whether
``end()`` is re-evaluted on each loop iteration. One common mistake is to
write a loop in this style:

.. code-block:: c++

  BasicBlock *BB = ...
  for (auto I = BB->begin(); I != BB->end(); ++I)
    ... use I ...
-->

#### ループで毎回`end()`を評価しない

range-based ``for``ループが使えず、イテレータを明示するループを書かざるを得ない場合、毎ループ``end()``が再評価されないか細心の注意を払ってください。
よくある間違いは、このようなスタイルで書くことです。

```cpp:悪いループスタイル
BasicBlock *BB = ...
for (auto I = BB->begin(); I != BB->end(); ++I)
  ... use I ...
```

<!--
The problem with this construct is that it evaluates "``BB->end()``" every time
through the loop.  Instead of writing the loop like this, we strongly prefer
loops to be written so that they evaluate it once before the loop starts.  A
convenient way to do this is like so:

.. code-block:: c++

  BasicBlock *BB = ...
  for (auto I = BB->begin(), E = BB->end(); I != E; ++I)
    ... use I ...
-->

この構造の問題は、ループ毎に"``BB->end()``"が評価されてしまうことです。このようなループではなく、ループ前に一度だけ評価するような書き方を強くお勧めします。

```cpp:ループ前に一度だけ評価する便利な方法
BasicBlock *BB = ...
for (auto I = BB->begin(), E = BB->end(); I != E; ++I)
  ... use I ...
```

<!--
The observant may quickly point out that these two loops may have different
semantics: if the container (a basic block in this case) is being mutated, then
"``BB->end()``" may change its value every time through the loop and the second
loop may not in fact be correct.  If you actually do depend on this behavior,
please write the loop in the first form and add a comment indicating that you
did it intentionally.
-->

注意深い方は、これら2つのループが異なるセマンティクスを持つ可能性にお気付きかもしれません。もしコンテナ（この例ではBasicBlock)が変更されるとしたら、"``BB->end()``"はループ毎に変わるかもしれず、2つ目のループ（訳注：事前評価）は正しくないかもしれません。実際そのような挙動に依存している場合は、最初の形式でループを書き、「意図的に毎ループ評価している」旨コメント追加してください。

<!--
Why do we prefer the second form (when correct)?  Writing the loop in the first
form has two problems. First it may be less efficient than evaluating it at the
start of the loop.  In this case, the cost is probably minor --- a few extra
loads every time through the loop.  However, if the base expression is more
complex, then the cost can rise quickly.  I've seen loops where the end
expression was actually something like: "``SomeMap[X]->end()``" and map lookups
really aren't cheap.  By writing it in the second form consistently, you
eliminate the issue entirely and don't even have to think about it.
-->

なぜ2つ目の形式がよいのか（正しい場合）？　最初の形式でループを書くことには2つの問題があります。第一に、ループ開始時に評価する方法と比べ、非効率かもしれません。この例では、コストはおそらくわずかですが、ループ毎に少し余分な負荷があります。しかしもっと複雑な式になると、コストが急上昇するかもしれません。"``SomeMap[X]->end()``"のような式を見たことがあります。mapのルックアップはけっして安くありません。2つ目の書き方を一貫することで、問題を完全に排除でき、考えずに済みます。

<!--
The second (even bigger) issue is that writing the loop in the first form hints
to the reader that the loop is mutating the container (a fact that a comment
would handily confirm!).  If you write the loop in the second form, it is
immediately obvious without even looking at the body of the loop that the
container isn't being modified, which makes it easier to read the code and
understand what it does.

While the second form of the loop is a few extra keystrokes, we do strongly
prefer it.
-->

さらに大きな第二の問題は、最初の形式で書くことはループ内でコンテナを変更していることを示すということです（コメントは簡単な確認という事実！）。2つ目の形式でループを書けば、コンテナは変更されないことがループ内を見ずとも分かります。

2つ目の形式でのループでは余分なキータイプはありますが、強くお勧めします。

<!--
``#include <iostream>`` is Forbidden
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The use of ``#include <iostream>`` in library files is hereby **forbidden**,
because many common implementations transparently inject a `static constructor`_
into every translation unit that includes it.

Note that using the other stream headers (``<sstream>`` for example) is not
problematic in this regard --- just ``<iostream>``. However, ``raw_ostream``
provides various APIs that are better performing for almost every use than
``std::ostream`` style APIs.

.. note::

  New code should always use `raw_ostream`_ for writing, or the
  ``llvm::MemoryBuffer`` API for reading files.

.. _raw_ostream:
-->

#### `#include <iostream>`禁止

ライブラリファイルで`#include <iostream>`を使うことは**禁止**されています。なぜなら、多くの一般的な実装では、それを含むすべての変換単位に静的コンストラクタを透過的に注入するからです。

それ以外のストリームヘッダ（たとえば`<sstream>`）の使用はこの点で問題ないことに注意してください。`<iostream>`のみです。しかし、`raw_ostream`の提供するさまざまなAPIは、ほとんどすべての用途で`std::ostream`スタイルのAPIよりも優れたパフォーマンスを発揮します。

:::note
新規コードでは常に、ファイル読み込みに`llvm::MemoryBuffer`APIを、書き込みにraw_ostreamを使ってください。
:::

<!--
Use ``raw_ostream``
^^^^^^^^^^^^^^^^^^^

LLVM includes a lightweight, simple, and efficient stream implementation in
``llvm/Support/raw_ostream.h``, which provides all of the common features of
``std::ostream``.  All new code should use ``raw_ostream`` instead of
``ostream``.

Unlike ``std::ostream``, ``raw_ostream`` is not a template and can be forward
declared as ``class raw_ostream``.  Public headers should generally not include
the ``raw_ostream`` header, but use forward declarations and constant references
to ``raw_ostream`` instances.
-->

#### `raw_ostream`を使う

LLVMは軽量で、シンプルで、かつ効率的なストリーム実装を`llvm/Support/raw_ostream.h`に持ちます。これは`std::ostream`の共通機能をすべて提供します。すべての新規コードで`ostream`ではなく`raw_ostream`を使ってください。

`std::ostream`と異なり、`raw_ostream`はテンプレートではありません。そのため`class raw_ostream`のように前方宣言できます。公開ヘッダには通常`raw_ostream`ヘッダを含めず、代わりに`raw_ostream`インスタンスへの前方宣言と定数参照を使います。

<!--
Avoid ``std::endl``
^^^^^^^^^^^^^^^^^^^

The ``std::endl`` modifier, when used with ``iostreams`` outputs a newline to
the output stream specified.  In addition to doing this, however, it also
flushes the output stream.  In other words, these are equivalent:

.. code-block:: c++

  std::cout << std::endl;
  std::cout << '\n' << std::flush;

Most of the time, you probably have no reason to flush the output stream, so
it's better to use a literal ``'\n'``.
-->

#### `std::endl`を避ける

`std::endl`修飾子は、`iostream`とともに使われ、指定の出力ストリームに改行を出力します。そして、出力ストリームをFlashします。言い換えると、以下は同等です。

```cpp
std::cout << std::endl;
std::cout << '\n' << std::flush;
```

ほとんどの場合、おそらく出力ストリームをFlashする理由はありません。`'\n'`リテラルを使うことをお勧めします。

<!--
Don't use ``inline`` when defining a function in a class definition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A member function defined in a class definition is implicitly inline, so don't
put the ``inline`` keyword in this case.

Don't:

.. code-block:: c++

  class Foo {
  public:
    inline void bar() {
      // ...
    }
  };

Do:

.. code-block:: c++

  class Foo {
  public:
    void bar() {
      // ...
    }
  };
-->

#### クラス定義内の関数定義で`inline`を使わない

クラス定義内で定義されたメンバー関数は暗黙的にインラインであるため、`inline`キーワードを入れないでください。

```cpp:禁止
class Foo {
public:
  inline void bar() {
    // ...
  }
};
```

```cpp:推奨
class Foo {
public:
  void bar() {
    // ...
  }
};
```

<!--

Microscopic Details
-------------------

This section describes preferred low-level formatting guidelines along with
reasoning on why we prefer them.
-->

### 細かい話

このセクションでは、推奨する低レベルのフォーマットガイドラインを、私たちが好む理由とともに説明します。

<!--
Spaces Before Parentheses
^^^^^^^^^^^^^^^^^^^^^^^^^

Put a space before an open parenthesis only in control flow statements, but not
in normal function call expressions and function-like macros.  For example:

.. code-block:: c++

  if (X) ...
  for (I = 0; I != 100; ++I) ...
  while (LLVMRocks) ...

  somefunc(42);
  assert(3 != 4 && "laws of math are failing me");

  A = foo(42, 92) + bar(X);

The reason for doing this is not completely arbitrary.  This style makes control
flow operators stand out more, and makes expressions flow better.
-->

#### 括弧の前にスペース

フロー制御文の開き括弧の前でのみスペースを入れます。普通の関数呼び出しや関数風マクロでは入れません。

```cpp:例
if (X) ...
for (I = 0; I != 100; ++I) ...
while (LLVMRocks) ...

somefunc(42);
assert(3 != 4 && "laws of math are failing me");

A = foo(42, 92) + bar(X);
```

このスタイルは、制御フロー演算子を目立たせ、式の流れを良くします。

<!--
Prefer Preincrement
^^^^^^^^^^^^^^^^^^^

Hard fast rule: Preincrement (``++X``) may be no slower than postincrement
(``X++``) and could very well be a lot faster than it.  Use preincrementation
whenever possible.

The semantics of postincrement include making a copy of the value being
incremented, returning it, and then preincrementing the "work value".  For
primitive types, this isn't a big deal. But for iterators, it can be a huge
issue (for example, some iterators contains stack and set objects in them...
copying an iterator could invoke the copy ctor's of these as well).  In general,
get in the habit of always using preincrement, and you won't have a problem.
-->

#### 前置インクリメントの選好

前置インクリメント（`++X'）は後置インクリメント（`X++`）よりも遅くなることはありません。むしろはるかに速くなる可能性があります。可能な限り前置インクリメントを使いましょう。

後置インクリメントは次の3つの内容を含みます。

1. インクリメントされる値のコピーを作成する
1. 「作業値」を前置インクリメントする
1. インクリメント前の値を返す

プリミティブ型の場合、これは大きな問題ではありません。しかしイテレータでは、大きな問題となる可能性があります。たとえば、いくつかのイテレータはスタックを含み、それらにオブジェクトを設定します。イテレータをコピーすると、それらのコピーコンストラクタを呼ぶことにもなります。一般に、いつも前置インクリメントを使う習慣を身につれば、問題は起きません。

<!--
Namespace Indentation
^^^^^^^^^^^^^^^^^^^^^

In general, we strive to reduce indentation wherever possible.  This is useful
because we want code to `fit into 80 columns`_ without excessive wrapping, but
also because it makes it easier to understand the code. To facilitate this and
avoid some insanely deep nesting on occasion, don't indent namespaces. If it
helps readability, feel free to add a comment indicating what namespace is
being closed by a ``}``.  For example:

.. code-block:: c++

  namespace llvm {
  namespace knowledge {

  /// This class represents things that Smith can have an intimate
  /// understanding of and contains the data associated with it.
  class Grokable {
  ...
  public:
    explicit Grokable() { ... }
    virtual ~Grokable() = 0;

    ...

  };

  } // namespace knowledge
  } // namespace llvm
-->

#### 名前空間のインデント

通常、私たちは可能な限りインデントを減らすよう努めています。これはコードを過度な折り返しなしで[80桁に収める](#ソースコードの幅)ためのみならず、コードを理解しやすくすることにも便利です。これを促すため、そして場合によって非常に深くなるネストを避けるため、名前空間はインデントしません。読みやすくなる場合、`}`でどの名前空間が閉じられるかをコメントしてもよいでしょう。

```cpp:例
namespace llvm {
namespace knowledge {

/// This class represents things that Smith can have an intimate
/// understanding of and contains the data associated with it.
class Grokable {
...
public:
  explicit Grokable() { ... }
  virtual ~Grokable() = 0;

  ...

};

} // namespace knowledge
} // namespace llvm
```

<!--
Feel free to skip the closing comment when the namespace being closed is
obvious for any reason. For example, the outer-most namespace in a header file
is rarely a source of confusion. But namespaces both anonymous and named in
source files that are being closed half way through the file probably could use
clarification.

.. _static:
-->

閉じられる名前空間が自明であれば終了コメントを省いてもよいでしょう。たとえば、ヘッダファイル内の最も外側の名前空間はまず混乱の原因となりません。しかし、ソースファイルの途中で名前空間（名前の有無を問わず）を閉じる場合は、説明したほうがよいでしょう。

<!--
Anonymous Namespaces
^^^^^^^^^^^^^^^^^^^^

After talking about namespaces in general, you may be wondering about anonymous
namespaces in particular.  Anonymous namespaces are a great language feature
that tells the C++ compiler that the contents of the namespace are only visible
within the current translation unit, allowing more aggressive optimization and
eliminating the possibility of symbol name collisions.  Anonymous namespaces are
to C++ as "static" is to C functions and global variables.  While "``static``"
is available in C++, anonymous namespaces are more general: they can make entire
classes private to a file.

The problem with anonymous namespaces is that they naturally want to encourage
indentation of their body, and they reduce locality of reference: if you see a
random function definition in a C++ file, it is easy to see if it is marked
static, but seeing if it is in an anonymous namespace requires scanning a big
chunk of the file.
-->

#### 無名名前空間

一般的に名前空間の話をした後は、特に無名名前空間について気になるでしょう。無名名前空間は偉大な言語機能です。名前空間の内容が現在の翻訳単位でのみでしか見えないことをC++コンパイラに伝え、より積極的な最適化を可能にし、シンボル名の衝突の可能性を排除します。C++の無名名前空間は、Cの関数とグローバル変数での「static」に似ています。C++でも「`static`」は使えますが、無名名前空間のほうが一般的です。これはファイルに対してクラス全体を非公開にできます。

無名名前空間の問題は、本来的に本文のインデントを求めることと、参照の局所性を減らすことです。C++ファイルのrandom関数の定義を見る場合、それがstaticかどうかは簡単に分かります。無名名前空間にあるかどうかを知るには、ファイル全体を調べる必要があります。

<!--
Because of this, we have a simple guideline: make anonymous namespaces as small
as possible, and only use them for class declarations.  For example:

.. code-block:: c++

  namespace {
  class StringSort {
  ...
  public:
    StringSort(...)
    bool operator<(const char *RHS) const;
  };
  } // anonymous namespace

  static void runHelper() {
    ...
  }

  bool StringSort::operator<(const char *RHS) const {
    ...
  }
-->

このため、シンプルなガイドラインがあります。無名名前空間はできるだけ小さくし、クラス定義にのみ使います。

```cpp:例
namespace {
class StringSort {
...
public:
  StringSort(...)
  bool operator<(const char *RHS) const;
};
} // anonymous namespace

static void runHelper() {
  ...
}

bool StringSort::operator<(const char *RHS) const {
  ...
}
```

<!--
Avoid putting declarations other than classes into anonymous namespaces:

.. code-block:: c++

  namespace {

  // ... many declarations ...

  void runHelper() {
    ...
  }

  // ... many declarations ...

  } // anonymous namespace
-->

クラス以外の宣言は匿名名前空間に入れません。

```cpp
namespace {

// ... many declarations ...

void runHelper() {
  ...
}

// ... many declarations ...

} // anonymous namespace
```

<!--
When you are looking at "``runHelper``" in the middle of a large C++ file,
you have no immediate way to tell if this function is local to the file.  In
contrast, when the function is marked static, you don't need to cross-reference
faraway places in the file to tell that the function is local.
-->

大きなC++ファイルの途中の「`runHelper`」を見た場合、ファイルローカルかどうかはすぐに判断できません。しかしstaticと明示されていれば、ローカルなのか知るためにファイル内の遠くを見なくて済みます。

<!--
Don't Use Braces on Simple Single-Statement Bodies of if/else/loop Statements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-->

#### 単純なif/else/loop文では中括弧を使わない

<!--
When writing the body of an ``if``, ``else``, or loop statement, we prefer to
omit the braces to avoid unnecessary line noise. However, braces should be used
in cases where the omission of braces harm the readability and maintainability
of the code.

We consider that readability is harmed when omitting the brace in the presence
of a single statement that is accompanied by a comment (assuming the comment
can't be hoisted above the ``if`` or loop statement, see below).
Similarly, braces should be used when a single-statement body is complex enough
that it becomes difficult to see where the block containing the following
statement began. An ``if``/``else`` chain or a loop is considered a single
statement for this rule, and this rule applies recursively.
-->

``if``/``else``やループ文の本体を書く場合、不要なラインノイズを避けるために中括弧を省くことが望ましいです。ただし、その省略によりコードの読みやすさ（readability）と保守性（maintainability）が損われる場合は中括弧を使わなくてはなりません。

読みやすさ（readability）が損なわれるのは、単一文にコメントがついている場合と考えられます（コメントを``if``やループ文の前に巻き上げられないと仮定します。以下も参照）。本体の単一文が十分に複雑な場合も同様で、文を含むブロックの始まりが分かりづらくなります。このような場合は中括弧を使います。このルールでは``if``/``else``チェインやループも単一文とみなし、再帰的に適用します。

<!--
This list is not exhaustive, for example, readability is also harmed if an
``if``/``else`` chain does not use braced bodies for either all or none of its
members, with complex conditionals, deep nesting, etc. The examples below
intend to provide some guidelines.

Maintainability is harmed if the body of an ``if`` ends with a (directly or
indirectly) nested ``if`` statement with no ``else``. Braces on the outer ``if``
would help to avoid running into a "dangling else" situation.
-->

このリストは不十分です。たとえば、複雑な条件や深い入れ子などを持った``if``/``else``チェインで中括弧をまばらに使うと読みにくくなります。以下の例でいくつかのガイドラインを示します。

保守性（maintainability）が損なわれるのは、``if``の本体が（直接的/間接的に）ネストされた``else``なしの``if``文で終わる場合です。外側の``if``への中括弧は、「ぶら下がりelse（dangling else）」問題を避ける役に立ちます。

<!--
.. code-block:: c++
  // Omit the braces, since the body is simple and clearly associated with the if.
  if (isa<FunctionDecl>(D))
    handleFunctionDecl(D);
  else if (isa<VarDecl>(D))
    handleVarDecl(D);

  // Here we document the condition itself and not the body.
  if (isa<VarDecl>(D)) {
    // It is necessary that we explain the situation with this surprisingly long
    // comment, so it would be unclear without the braces whether the following
    // statement is in the scope of the `if`.
    // Because the condition is documented, we can't really hoist this
    // comment that applies to the body above the if.
    handleOtherDecl(D);
  }

  // Use braces on the outer `if` to avoid a potential dangling else situation.
  if (isa<VarDecl>(D)) {
    for (auto *A : D.attrs())
      if (shouldProcessAttr(A))
        handleAttr(A);
  }

  // Use braces for the `if` block to keep it uniform with the else block.
  if (isa<FunctionDecl>(D)) {
    handleFunctionDecl(D);
  } else {
    // In this else case, it is necessary that we explain the situation with this
    // surprisingly long comment, so it would be unclear without the braces whether
    // the following statement is in the scope of the `if`.
    handleOtherDecl(D);
  }

  // This should also omit braces.  The `for` loop contains only a single statement,
  // so it shouldn't have braces.  The `if` also only contains a single simple
  // statement (the for loop), so it also should omit braces.
  if (isa<FunctionDecl>(D))
    for (auto *A : D.attrs())
      handleAttr(A);

  // Use braces for the outer `if` since the nested `for` is braced.
  if (isa<FunctionDecl>(D)) {
    for (auto *A : D.attrs()) {
      // In this for loop body, it is necessary that we explain the situation
      // with this surprisingly long comment, forcing braces on the `for` block.
      handleAttr(A);
    }
  }

  // Use braces on the outer block because there are more than two levels of nesting.
  if (isa<FunctionDecl>(D)) {
    for (auto *A : D.attrs())
      for (ssize_t i : llvm::seq<ssize_t>(count))
         handleAttrOnDecl(D, A, i);
  }

  // Use braces on the outer block because of a nested `if`, otherwise the
  // compiler would warn: `add explicit braces to avoid dangling else`
  if (auto *D = dyn_cast<FunctionDecl>(D)) {
    if (shouldProcess(D))
      handleVarDecl(D);
    else
      markAsIgnored(D);
  }
-->

```cpp
// 中括弧を省きます。本体は単純で、ifとの関係も明確です。
if (isa<FunctionDecl>(D))
  handleFunctionDecl(D);
else if (isa<VarDecl>(D))
  handleVarDecl(D);


// ここは条件についてのコメントです。本体部分についてではなく。
if (isa<VarDecl>(D)) {
  // この驚くほど長いコメントで状況を説明する必要がありますが、
  // 中括弧がないと次の文が`if`スコープ内かどうか分かりません。
  // 既に条件のコメントがあるため、本体に関するこのコメントを
  // ifの前に巻き上げることはできません。
  handleOtherDecl(D);
}

// 外側の`if`に中括弧を使い、ぶら下がりelseの可能性を避けます。
if (isa<VarDecl>(D)) {
  for (auto *A : D.attrs())
    if (shouldProcessAttr(A))
      handleAttr(A);
}

// `if`ブロックに中括弧を使い、elseブロックと同じ形を保ちます。
if (isa<FunctionDecl>(D)) {
  handleFunctionDecl(D);
} else {
  // このelseの場合も、この驚くほど長いコメントで状況を
  // 説明する必要がありますが、中括弧がないと次の文が
  // `if`スコープ内かどうか分かりません。
  handleOtherDecl(D);
}

// これは中括弧を省略するべきです。`for`ループは単一文しか含まないため、
// 中括弧を持つべきではありません。`if`も単一文（ループ）しか含まないので、
// 同じく中括弧は省くべきです。
if (isa<FunctionDecl>(D))
  for (auto *A : D.attrs())
    handleAttr(A);

// ネストされた`for`が囲われているため、外側の`if`も囲みます。
if (isa<FunctionDecl>(D)) {
  for (auto *A : D.attrs()) {
    // このループ本文内では、この驚くほど長いコメントで状況を
    // 説明し、`for`ブロックに中括弧を強制する必要があります。
    handleAttr(A);
  }
}

// ２階層以上のネストがあるため、外側のブロックに中括弧を使います。
if (isa<FunctionDecl>(D)) {
  for (auto *A : D.attrs())
    for (ssize_t i : llvm::seq<ssize_t>(count))
        handleAttrOnDecl(D, A, i);
}

// ネストされた`if`の外側のブロックには中括弧を使います。
// さもないとコンパイラに警告されます:
// `add explicit braces to avoid dangling else`
if (auto *D = dyn_cast<FunctionDecl>(D)) {
  if (shouldProcess(D))
    handleVarDecl(D);
  else
    markAsIgnored(D);
}
```

<!--

See Also
========

A lot of these comments and recommendations have been culled from other sources.
Two particularly important books for our work are:

#. `Effective C++
   <http://www.amazon.com/Effective-Specific-Addison-Wesley-Professional-Computing/dp/0321334876>`_
   by Scott Meyers.  Also interesting and useful are "More Effective C++" and
   "Effective STL" by the same author.

#. `Large-Scale C++ Software Design
   <http://www.amazon.com/Large-Scale-Software-Design-John-Lakos/dp/0201633620/ref=sr_1_1>`_
   by John Lakos

If you get some free time, and you haven't read them: do so, you might learn
something.
-->

## 関連項目

これらのコメントや勧告の多くはほかの情報源から抜粋されています。特に重要な書籍を紹介します。

1. [Effective C++](http://www.amazon.com/Effective-Specific-Addison-Wesley-Professional-Computing/dp/0321334876) by Scott Meyers。同じ著者による「More Effective C++」「Effective STL」もまた、興味深く有用です。
1. [Large-Scale C++ Software Design](http://www.amazon.com/Large-Scale-Software-Design-John-Lakos/dp/0201633620/ref=sr_1_1) by John Lakos

----

## 原文の変更内容

リンク先の更新や文言修正など内容に関わらない変更は記載省略してます。

### 13.0.0 -> 14.0.0

変更なし。コーディング標準としては記載がありませんが、サポートするVisual Studioが2017->2019になっています。

### 12.0.0 -> 13.0.0

変更なし。

### 11.0.0 -> 12.0.0

- 追加：機械的なソースの問題＞ソースコードのフォーマット＞コメント＞ヘッダガード
- 例拡充：スタイルの問題＞細かい話＞単純なif/else/loop文では中括弧を使わない

### 10.0.0 -> 11.0.0

- 追加：機械的なソースの問題＞ソースコードのフォーマット＞エラーと警告メッセージ
- 追加：スタイルの問題＞高位の問題＞宣言された関数の実装には名前空間修飾子を用いる
- 文言追加：スタイルの問題＞低位の問題＞できるだけrange-based ``for``ループを使う
　``std::for_each()``/``llvm::for_each()``の非推奨を明記
- 追加：スタイルの問題＞細かい話＞単純なif/else/loop文では中括弧を使わない

### 9.0.0 -> 10.0.0

ベースがC++11→C++14に変わりました。文章が大きく整理されました。

- 再構成：前書き＞言語、ライブラリ、および標準
　C++11→C++14に。
- 削除：機械的なソースの問題＞ソースコードのフォーマット＞インデントの一環
- 内容追加：機械的なソースの問題＞言語とコンパイラの問題＞コードを読みやすくするために`auto`型推論を使う
　ジェネリックラムダについて。

### 8.0.0 -> 9.0.0

- 内容変更：機械的なソースの問題＞ソースコードのフォーマット＞ファイルのヘッダ
　標準様式変更。ライセンスについて。

### 7.0.0 -> 8.0.0

- 内容追加：機械的なソースの問題＞ソースコードのフォーマット＞コメント書式
　C++スタイルの例外として、パラメータの場合。
- 見出し変更と内容追加：機械的なソースの問題＞ソースコードのフォーマット＞空白（前版では「タブの代わりにスペースを使う」）
　行末の空白について。

### 6.0.0 -> 7.0.0

- 追加：機械的なソースの問題＞言語とコンパイラの問題＞等しい要素のソートによる非決定性に注意
- 削除（下2つに分割）：スタイルの問題＞高位の問題＞公開ヘッダファイルはモジュール
- 追加：スタイルの問題＞高位の問題＞自己完結型ヘッダ
- 追加：スタイルの問題＞高位の問題＞ライブラリの階層化

### 5.0.1 -> 6.0.0

- 追加：機械的なソースの問題＞言語とコンパイラの問題＞ポインタ順序による非決定性に注意
- 変更：スタイルの問題＞高位の問題＞早期終了と`continue`でコードをシンプルに
　コードがシンプルに（range-based for, auto）
- 内容追加：スタイルの問題＞低位の問題＞たっぷりのアサート
　エラーの回復について。
- 追加：スタイルの問題＞低位の問題＞できるだけrange-based ``for``ループを使う
- 内容変更：スタイルの問題＞低位の問題＞ループで毎回`end()`を評価しない

## この文書（翻訳）のライセンスについて

© Copyright 2003-2022, LLVM Project.
原文は[こちらのライセンス](https://releases.llvm.org/14.0.0/LICENSE.TXT)下にあるLLVMのドキュメントに含まれているため、そちらのライセンスに従います。
翻訳者（@tenmyo）は著作権を主張しません。
