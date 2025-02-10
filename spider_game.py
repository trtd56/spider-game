import pyxel

class App:
    def __init__(self):
        # 画面サイズを設定 (幅, 高さ)
        pyxel.init(160, 120, title="Spider Game")
        pyxel.load("myspider.pyxres")

        # 必要な変数の初期化
        self.reset()

        # メインループを開始
        pyxel.run(self.update, self.draw)

    def reset(self):
        # 蜘蛛の位置や状態
        self.spider_x = 80
        self.spider_y = 0
        self.spider_is_descending = False
        self.spider_speed = 2

        # 虫のリスト (x, y) などで管理
        self.insects = []
        self.insect_speed = 1

        # スコアやタイマー
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 60  # 何フレームごとに虫を出すか (60 なら1秒おき)

    def update(self):
        """
        1フレームごとに呼び出されるゲームロジックの更新処理
        """
        # [1] 入力処理
        self.handle_input()

        # [2] 蜘蛛の移動
        self.update_spider()

        # [3] 虫の生成と移動
        self.spawn_insects()
        self.update_insects()

        # [4] 当たり判定
        self.check_collision()

    def handle_input(self):
        """
        プレイヤーからの入力（マウス・キーボード）を処理
        """
        # Pyxel は標準でマウス入力をサポートします (ver1.6以降)
        # 左クリックが押された瞬間を検知
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # 蜘蛛が降下開始
            self.spider_is_descending = True

        # (オプション) キーボードのスペースで同じような動作を入れてもOK
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.spider_is_descending = True

    def update_spider(self):
        """
        蜘蛛の上下移動を更新
        """
        if self.spider_is_descending:
            # 下に降りる
            self.spider_y += self.spider_speed
            # 一定の位置 (画面下部) で止めたり戻したり
            if self.spider_y > 100:
                self.spider_is_descending = False
        else:
            # 上に戻る
            if self.spider_y > 0:
                self.spider_y -= self.spider_speed
            else:
                self.spider_y = 0

    def spawn_insects(self):
        """
        一定間隔で虫を生成する
        """
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            # 虫を左端に生成 (y 座標は少しランダム)
            y_pos = pyxel.rndi(70, 110)
            self.insects.append({
                "x": 0,
                "y": y_pos
            })

    def update_insects(self):
        """
        生成した虫たちを右方向へ移動させる
        """
        for insect in self.insects:
            insect["x"] += self.insect_speed

        # 画面外に出た虫を削除
        self.insects = [i for i in self.insects if i["x"] < 160]

    def check_collision(self):
        """
        蜘蛛と虫の衝突判定を行い、当たった虫を削除してスコア加算
        """
        # 蜘蛛のヒットボックス（適当に 8x8 くらい）を考慮して単純な矩形衝突で判定
        spider_left   = self.spider_x - 4
        spider_right  = self.spider_x + 4
        spider_top    = self.spider_y - 4
        spider_bottom = self.spider_y + 4

        new_insect_list = []
        for insect in self.insects:
            insect_left   = insect["x"] - 4
            insect_right  = insect["x"] + 4
            insect_top    = insect["y"] - 4
            insect_bottom = insect["y"] + 4

            # 矩形が重なっているかどうか
            if (spider_right  >= insect_left  and
                spider_left   <= insect_right and
                spider_bottom >= insect_top   and
                spider_top    <= insect_bottom):
                # 衝突した => スコア加算、虫を消す
                self.score += 1
                # 蜘蛛を上に戻す・降下終了
                self.spider_is_descending = False
            else:
                # 衝突していない => 存続
                new_insect_list.append(insect)

        self.insects = new_insect_list

    def draw(self):
        # 背景のクリア (白背景の場合: pyxel.cls(7))
        pyxel.cls(0)

        # ❶ 蜘蛛の糸を描画
        #   例として、x は spider_x、y は spider_y + 3 (少し下寄り = 蜘蛛のお尻あたり)
        #   から画面上端 (spider_x, 0) へ伸ばす線を描画
        pyxel.line(
            self.spider_x,        # 始点X
            self.spider_y + 3,    # 始点Y (蜘蛛の尻を想定)
            self.spider_x,        # 終点X (同じX座標)
            0,                    # 終点Y (画面上)
            7                     # カラー (0=黒、または1, 2, ... お好みで)
        )

        # ❷ 蜘蛛本体を描く (四角で代用)
        # 例：蜘蛛画像を 16x16 で描いている場合（左上(0,0)）
        pyxel.blt(
            self.spider_x - 8,  # 蜘蛛の半径分ずらす
            self.spider_y - 8,
            0,     # 画像バンク (pyxel.load で読み込んだ先頭バンク)
            0, 0,  # バンク画像内の取り出し開始位置
            16, 16,# サイズ (幅, 高さ)
            0     # 透過色 (ピクセルエディタで背景色を0にしている場合)
        )

        # ❸ 虫の描画 (例)
        for insect in self.insects:
            pyxel.blt(
                insect["x"] - 8,  # 蜘蛛の半径分ずらす
                insect["y"] - 8,
                0,     # 画像バンク (pyxel.load で読み込んだ先頭バンク)
                16, 0,  # バンク画像内の取り出し開始位置
                16, 16,# サイズ (幅, 高さ)
                0     # 透過色 (ピクセルエディタで背景色を0にしている場合)
            )

        # スコア表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)  # 色0=黒文字

# 実行
App()
