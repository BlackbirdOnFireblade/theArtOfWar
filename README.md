# 軍師電卓

とりあえず・・・版

--
# セットアップ
miniconda( https://docs.conda.io/en/latest/miniconda.html )をインストール
・Windowsの場合
スタートメニュー ⇒ Anaconda3 ⇒ Anaconda Prompt を起動
conda install matplotlib
を叩く
ソース一式、適当なとこに置く

# 起動
cd 上記フォルダ
python main.py -o 2.0.1 -d 3.0.0 -r 2000

## コマンドライン引数
-o 攻撃する拠点数をドット区切りで、赤.青.金 (ex) -o 2.0.1
-d 防御する拠点数をドット区切りで、赤.青.金 (ex) -d 3.0.0
-r 自軍リソース(おにぎり) (ex) -r 2000

## その他コマンドライン引数
--resolution 時間解像度、1minを何分割するか。default 2(30s) (ex) --resolution 4
--timerate 1枚抜くのにかかる平均時間(秒)。default 1.8 (ex) --timerate 1.5
--unit 防衛最低枚数をドット区切りで、赤.青.金。 default 2.2.3 (ex) --unit 1.1.2
--resource_step リソースグラフの増減調整量。 default 100 (ex) --resource_step 50

# 使い方
左側グラフをクリックで防衛開始して、防衛時間を引くと右側でリソース推移を表示
防衛ラインを再度クリックすると、そこの時間で中断
防衛ラインを右クリックすると、ライン削除

防衛ラインは、クリックした時間から最後まで引きます。
（すでに防衛ラインが引かれていればそこまでの追加）
複数ラインが連続している箇所は、mキーでマージされます。

qキーで終了
--

まだまだ粗削りです。
