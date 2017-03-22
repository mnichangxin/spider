var _Pwin = null;
var _fbz = false;
window.ToInitMedia = function (_win) {
    _Pwin = _win;
    _win.Form1.mediaUrl.value = ____de($("#hfWareUrl").val());
    _win.Starttime = $("#hfLastPos").val();
    _win.InitMedia()
};

function btnClose_onclick() {
    if (_Pwin == null) {
        return
    };
    _Pwin.timelimit = 0;
    var _pos = _Pwin.document.MediaPlayer.GetPosition();
    var _totaltime = _Pwin.totaltime;
    $.post("RecordStudyInfo.ashx", {
        studyInfoId: $("#hfStudyInfoId").val(),
        pos: _pos,
        totaltime: _totaltime,
        actionType: 'exit'
    }, function (resp) {});
    window.close()
};

function btnSavePos_onclick() {
    if (_Pwin == null) {
        alert("学习过程尚未加载。");
        return
    };
    _Pwin.timelimit = 0;
    var _pos = _Pwin.document.MediaPlayer.GetPosition();
    var _totaltime = _Pwin.totaltime;
    var _len = 0;
    if (_Pwin.document.MediaPlayer.GetPlayState() == 3) _len = _Pwin.document.MediaPlayer.GetLength();
    $.post("RecordStudyInfo.ashx", {
        studyInfoId: $("#hfStudyInfoId").val(),
        pos: _pos,
        totaltime: _totaltime,
        medialength: _len
    }, function (resp) {
        var _state = _Pwin.document.MediaPlayer.GetPlayState();
        if (_state == 3) _Pwin.document.MediaPlayer.DoPause();
        Notify(resp);
        if (resp.toString().substr(0, 1) == 'N') {
            alert("操作失败：" + resp.toString().substring(2))
        } else {
            if (resp.toString() == 'Y:W') {
                if ($("#hfNWareId").val() != "") {
                    $("#divNextWareLink").show()
                }
            };
            alert("保存成功。")
        };
        if (_state == 3) {
            _Pwin.document.MediaPlayer.DoPlay()
        }
    })
};

window._finish = function () {
    if (_Pwin.document.MediaPlayer.GetPlayState() == 3) {
        if (_Pwin == null) {
            return
        };
        _Pwin.timelimit = 0;
        var _pos = _Pwin.document.MediaPlayer.GetPosition();
        var _len = _Pwin.document.MediaPlayer.GetLength();
        var _totaltime = _Pwin.totaltime;
        $.post("RecordStudyInfo.ashx", {
            studyInfoId: $("#hfStudyInfoId").val(),
            pos: _pos,
            totaltime: _totaltime,
            medialength: _len,
            actionType: 'f'
        }, function (resp) {
            Notify(resp);
            if (resp.toString() == 'Y:W') {
                _fbz = true;
                if ($("#hfNWareId").val() != "") {
                    $("#divNextWareLink").show()
                }
            }
        })
    }
};