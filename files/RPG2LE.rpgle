     H DFTACTGRP(*NO) ACTGRP(*NEW)
     H OPTION(*SRCSTMT : *NOUNREF : *NODEBUGIO)
     H DATEDIT(*YMD)
      *
      *ファイル定義
     FSYOHINL   UF A E           K DISK    INFDS(dbfds)
     F                                     INFSR(#DBEX)
     FDSPF2     CF   E             WORKSTN INDDS(ws)
      *
      *サブプロシージャー定義
     DsetMsg           PR
     D  msgType                       1    CONST
     D  msgText                            CONST LIKE(MSGDTA)
      *
      *データ構造、変数定義
     Ddbfds            DS
     D  dbfStatus             11     15
     D  dbfOpr           *OPCODE
      *
     Dws               DS                  QUALIFIED
     D  exit_03                        N   OVERLAY(ws : 3)
     D  prev_07                        N   OVERLAY(ws : 7)
     D  next_08                        N   OVERLAY(ws : 8)
     D  add_09                         N   OVERLAY(ws : 9)
     D  init_11                        N   OVERLAY(ws : 11)
     D  del_23                         N   OVERLAY(ws : 23)
     D  fldChange_30                   N   OVERLAY(ws : 30)
     D  dspCurMode_41_43...
     D                                3    OVERLAY(ws : 41)
     D  errorMsg_50                    N   OVERLAY(ws : 50)
     D  infoMsg_51                     N   OVERLAY(ws : 51)
     D  dspDetail_60                   N   OVERLAY(ws : 60)
     D  fieldRI_PR_61                  N   OVERLAY(ws : 61)
      *
     DdspMsg           S             50
     Dwait             S              1
     DreturnPt         S              6
      *
      *メイン処理
      /FREE

        SETLL(E) *LOVAL SYOHINR;
        EXSR #DBEX; //ＤＢエラー
        EXSR #INIT; //初期画面表示

        DOW (1 = 1);

          EXFMT DSPF2R;
          setMsg(' ' : ' ');

          SELECT;

            WHEN ws.exit_03;               // F3=終了
              LEAVE;

            WHEN ws.prev_07 OR ws.next_08; // F7=前/ F8=次
              ws.dspCurMode_41_43 = '100';
              IF ws.dspDetail_60;
                EXSR #UPDAT; //レコード更新
              ENDIF;
              IF NOT ws.errorMsg_50;
                EXSR #MOVE;  //次／前ページ
              ENDIF;

            WHEN ws.add_09;                // F9=挿入
              ws.dspCurMode_41_43 = '010';
              EXSR #ADD;  //レコード追加
              EXSR #INIT; //初期画面表示

            WHEN ws.init_11;               // F11=初期画面
              ws.dspCurMode_41_43 = '100';
              EXSR #INIT; //初期画面表示

            WHEN ws.del_23;                // F23=削除
              ws.dspCurMode_41_43 = '001';
              EXSR #DEL;  //レコード削除

            OTHER;                         // ENTER(実行)
              IF ws.dspDetail_60 AND ws.fldChange_30;
                EXSR #UPDAT; //レコード更新
              ELSE;
                EXSR #CHAIN; //キーで読み込み
              ENDIF;

          ENDSL;

        ENDDO;

        *INLR = *ON;
        RETURN;

        //サブルーチン

        //初期画面表示////////////////////////////////////
        BEGSR #INIT;

          //初期画面→明細非表示
          CLEAR SYOHINR;
          ws.dspDetail_60 = *OFF;  //明細非表示
          ws.dspCurMode_41_43 = '100';

        ENDSR;

        //レコード更新////////////////////////////////////
        BEGSR #UPDAT;

          //データが変更されていれば更新
          IF ws.fldChange_30;

            UPDATE(E) SYOHINR;

            //更新エラー→エラー表示、明細表示（現レコード）
            IF %ERROR;
              setMsg('E' : 'レコードの更新でエラー。' +
                     '(' + dbfOpr + ', ' + dbfStatus + ')');
              ws.dspDetail_60 = *ON;  //明細表示
            //更新正常終了→メッセージ表示、更新数+1
            ELSE;
              setMsg('I' : 'レコードが更新された。');
              UPDNUM += 1;
            ENDIF;

          ENDIF; //データ変更あり

        ENDSR;

        //次／前ページ////////////////////////////////////
        BEGSR #MOVE;

          //初期画面の場合は部分キーで位置づけ
          IF (NOT ws.dspDetail_60) AND (PRPRCD <> *BLANKS);
            SETLL(E) PRPRCD SYOHINR;
            EXSR #DBEX; //ＤＢエラー
          ENDIF;

          //前／後のレコード読み込み
          IF ws.prev_07;
            READP(E) SYOHINR;
          ELSE; // ws.next_08
            READ(E) SYOHINR;
          ENDIF;
          EXSR #DBEX; //ＤＢエラー

          //最初・最後のレコードを超えた→MSG表示
          IF %EOF;
            IF ws.prev_07;
              SETLL(E) *HIVAL SYOHINR;
            ELSE; // ws.next_08
              SETLL(E) *LOVAL SYOHINR;
            ENDIF;
            EXSR #DBEX; //ＤＢエラー
            setMsg('I' : '最初または最後のレコードを超えた。');
            EXSR #INIT;
          //エラーなし→MSG非表示、明細表示（移動先レコード）
          ELSE;
            ws.dspDetail_60 = *ON; //明細表示
          ENDIF;

        ENDSR;

        //レコード追加////////////////////////////////////
        BEGSR #ADD;

          //空レコードの表示
          CLEAR SYOHINR;
          ws.dspDetail_60 = *ON;  //明細表示

          //データの追加
          DOW (1 = 1);

            EXFMT DSPF2R;
            setMsg(' ' : ' ');

            //追加取消→MSG表示、初期画面
            IF ws.exit_03;
              setMsg('I' : 'レコードの追加が取り消された。');
              LEAVE;
            ENDIF;

            //キー未入力エラー→エラー表示、明細表示
            IF (NOT ws.errorMsg_50) AND (PRPRCD = *BLANKS);
              setMsg('E' : '製品コードが未入力。');
            ENDIF;

            //レコードの書出し
            IF NOT ws.errorMsg_50;

              WRITE(E) SYOHINR;

              //追加エラー→エラー表示、明細表示（現レコード）
              IF %ERROR;
                setMsg('E' : 'レコードの追加でエラー。' +
                       '(' + dbfOpr + ', ' + dbfStatus + ')');
              ELSE;
                //追加OK→追加モードの終了
                setMsg('I' : 'レコードが追加された。');
                ADDNUM += 1;
                //追加レコードに位置づけ
                SETLL(E) PRPRCD SYOHINR;
                EXSR #DBEX; //ＤＢエラー
                LEAVE;

              ENDIF; //追加エラー

            ENDIF; // NOT ws.errorMsg_50

          ENDDO;

        ENDSR;

        //レコード削除////////////////////////////////////
        BEGSR #DEL;

          //レコードの削除メッセージ表示
          setMsg('I' : 'レコードを削除するにはF23' +
                       '。F3または実行キーで取消。');
          ws.dspDetail_60 = *ON;  //明細表示
          ws.fieldRI_PR_61 = *ON; //フィールドの反転・保護

          //削除画面表示→F23で削除
          EXFMT DSPF2R;

          IF ws.del_23;

            DELETE(E) SYOHINR;

            //削除エラー→エラー表示、明細表示（現レコード）
            IF %ERROR;
              setMsg('E' : 'レコードの削除でエラー。' +
                       '(' + dbfOpr + ', ' + dbfStatus + ')');
              ws.dspDetail_60 = *ON;   //明細表示
              ws.fieldRI_PR_61 = *OFF; //フィールドの通常表示

            //削除完了→メッセージ表示、初期画面
            ELSE;
              setMsg('I' : 'レコードが削除された。');
              DLTNUM += 1;
              ws.fieldRI_PR_61 = *OFF; //フィールドの通常表示
              //削除レコードに位置づけ
              SETLL(E) PRPRCD SYOHINR;
              EXSR #DBEX; //ＤＢエラー
              EXSR #INIT;

            ENDIF;

          //削除取消→メッセージ表示、初期画面
          ELSE;
            setMsg('I' : 'レコードの削除が取り消された。');
            ws.fieldRI_PR_61 = *OFF; //フィールドの通常表示
            EXSR #INIT;

          ENDIF; // ws.del_23

        ENDSR;

        //レコードキー読み込み////////////////////////////
        BEGSR #CHAIN;

          CHAIN(E) PRPRCD SYOHINR;

          EXSR #DBEX; //ＤＢエラー
          //キーなしエラー→メッセージ表示、明細非表示
          IF NOT %FOUND;
            setMsg('E' : '商品コードが見つからない。');
            ws.dspDetail_60 = *OFF;   //明細非表示
          //キーあり→明細表示
          ELSE;
            ws.dspDetail_60 = *ON;    //明細表示
          ENDIF;

        ENDSR;

        // DB例外処理(INFSR) /////////////////////////////
        BEGSR #DBEX;

          IF %ERROR;
            dspMsg = 'ＤＢ入出力で回復不能エラー。' +
                         '(' + dbfOpr + ', ' + dbfStatus + ')';
            DSPLY dspMsg wait;
            returnPt = '*CANCL';
          ELSE;
            returnPt = *BLANKS;
          ENDIF;

        ENDSR returnPt;

      /END-FREE

        //サブプロシージャー

     PsetMsg           B
     DsetMsg           PI
     D  msgType                       1    CONST
     D  msgText                            CONST LIKE(MSGDTA)
      *
      /FREE

        ws.errorMsg_50 = *OFF;
        ws.infoMsg_51 = *OFF;

        IF msgType = 'E';
          ws.errorMsg_50 = *ON;
        ELSEIF msgType = 'I';
          ws.infoMsg_51 = *ON;
        ENDIF;

        MSGDTA = msgText;

        RETURN;

      /END-FREE
      *
     PsetMsg           E