' SJIS
' �ϐ��̐錾������
Option Explicit

Dim oWsh : Set oWsh = WScript.CreateObject("WScript.Shell")
Dim oFSO:Set oFSO = CreateObject("Scripting.FileSystemObject")
Dim fpath:fpath = oFSO.GetParentFolderName(WScript.ScriptFullName) & "\���[�N�V�[�g.xlsx"

' GetObject�Ńt�@�C���p�X��n���ƁA�i�Ȃ���ΐV���ɊJ���Ă���j�I�u�W�F�N�g��������
Dim oWb:set oWb = GetObject(fpath)
Call oWb.Activate ' �Ȃ��Ă�������
oWb.Windows(1).Visible = True
Call oWsh.AppActivate(oWb.Application.Caption)
' �����Ń}�N���Ƃ����낢����s����
