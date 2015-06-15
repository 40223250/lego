# coding=utf-8
# 上面的程式內容編碼必須在程式的第一或者第二行才會有作用

################# (1) 模組導入區
# 導入 cherrypy 模組, 為了在 OpenShift 平台上使用 cherrypy 模組, 必須透過 setup.py 安裝



import cherrypy
# 導入 Python 內建的 os 模組, 因為 os 模組為 Python 內建, 所以無需透過 setup.py 安裝
import os
# 導入 random 模組
import random
import math
from cherrypy.lib.static import serve_file
# 導入 gear 模組
#import gear
import man
import man2

################# (2) 廣域變數設定區
# 確定程式檔案所在目錄, 在 Windows 下有最後的反斜線
_curdir = os.path.join(os.getcwd(), os.path.dirname(__file__))
# 設定在雲端與近端的資料儲存目錄
if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示程式在雲端執行
    download_root_dir = os.environ['OPENSHIFT_DATA_DIR']
    data_dir = os.environ['OPENSHIFT_DATA_DIR']
else:
    # 表示程式在近端執行
    download_root_dir = _curdir + "/local_data/"
    data_dir = _curdir + "/local_data/"


def downloadlist_access_list(files, starti, endi):
    # different extension files, associated links were provided
    # popup window to view images, video or STL files, other files can be downloaded directly
    # files are all the data to list, from starti to endi
    # add file size
    outstring = ""
    for index in range(int(starti)-1, int(endi)):
        fileName, fileExtension = os.path.splitext(files[index])
        fileExtension = fileExtension.lower()
        fileSize = sizeof_fmt(os.path.getsize(download_root_dir+"downloads/"+files[index]))
        # images files
        if fileExtension == ".png" or fileExtension == ".jpg" or fileExtension == ".gif":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # stl files
        elif fileExtension == ".stl":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/static/viewstl.html?src=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # flv files
        elif fileExtension == ".flv":
            outstring += '<input type="checkbox" name="filename" value="'+files[index]+'"><a href="javascript:;" onClick="window.open(\'/flvplayer?filepath=/downloads/'+ \
            files[index]+'\',\'images\', \'catalogmode\',\'scrollbars\')">'+files[index]+'</a> ('+str(fileSize)+')<br />'
        # direct download files
        else:
            outstring += "<input type='checkbox' name='filename' value='"+files[index]+"'><a href='/download/?filepath="+download_root_dir.replace('\\', '/')+ \
            "downloads/"+files[index]+"'>"+files[index]+"</a> ("+str(fileSize)+")<br />"
    return outstring
def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')
################# (3) 程式類別定義區
# 以下改用 CherryPy 網際框架程式架構
# 以下為 Hello 類別的設計內容, 其中的 object 使用, 表示 Hello 類別繼承 object 的所有特性, 包括方法與屬性設計
class Midterm(object):

    # Midterm 類別的啟動設定
    _cp_config = {
    'tools.encode.encoding': 'utf-8',
    'tools.sessions.on' : True,
    'tools.sessions.storage_type' : 'file',
    #'tools.sessions.locking' : 'explicit',
    # session 以檔案儲存, 而且位於 data_dir 下的 tmp 目錄
    'tools.sessions.storage_path' : data_dir+'/tmp',
    # session 有效時間設為 60 分鐘
    'tools.sessions.timeout' : 60
    }

    def __init__(self):
        # hope to create downloads and images directories　
        if not os.path.isdir(download_root_dir+"downloads"):
            try:
                os.makedirs(download_root_dir+"downloads")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"images"):
            try:
                os.makedirs(download_root_dir+"images")
            except:
                print("mkdir error")
        if not os.path.isdir(download_root_dir+"tmp"):
            try:
                os.makedirs(download_root_dir+"tmp")
            except:
                print("mkdir error")
    # 以 @ 開頭的 cherrypy.expose 為 decorator, 用來表示隨後的成員方法, 可以直接讓使用者以 URL 連結執行
    @cherrypy.expose
    # index 方法為 CherryPy 各類別成員方法中的內建(default)方法, 當使用者執行時未指定方法, 系統將會優先執行 index 方法
    # 有 self 的方法為類別中的成員方法, Python 程式透過此一 self 在各成員方法間傳遞物件內容
    def index(self):
        outstring = '''
        <!DOCTYPE html> 
        <html>
        <head>
        LEGO 分別組立 第07組 <br /><br />

    <a href="body">身體組立</a><br />

     <a href="waist">褲子組立</a><br />

     <a href="right_leg">右腳組立</a><br />

     <a href="head">頭部組立</a><br /> 

    <a href="hat">帽子組立</a><br />

    <a href="left_leg">左腳組立</a><br />
       
     
    <a href=" right_hand">右手組立</a><br />

     
     <a href="left_hand">左手組立</a><br /> <br />     
   
    <a href="all">全部組立</a><br />

        </head>
        
        </html>
        '''
        
        return outstring
    @cherrypy.expose
    def body (self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////


    // Body 與空組立檔案採三個平面約束組立
    // 空組立面為 ASM_TOP, ASM_FRONT, ASM_RIGHT
    // Body 組立面為 TOP, FRONT, RIGHT
    // 若 featID=0 表示為空組立檔案, 而且函式會傳回第一個組立件的 featID

    var featID = three_plane_assembly(session, assembly, transf, 40, 0, "LEGO_BODY.prt", "ASM_TOP", "ASM_FRONT", "ASM_RIGHT", "TOP", "FRONT", "RIGHT"); 


    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
            return outstring
    @cherrypy.expose
    def left_hand(self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////


    // 利用函式呼叫組立左手 ARM, 組立增量次序為 2
    axis_plane_assembly(session, assembly, transf,40 , 0, 
                                  "LEGO_ARM_LT.prt", "A_9", "DTM2", "A_4", "DTM1");
                                  
     // 利用函式呼叫組立左手 HAND, 組立增量次序為 4
    axis_plane_assembly(session, assembly, transf, 40,8 , 
                                  "LEGO_HAND.prt", "A_2", "DTM2", "A_1", "DTM3");

    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
            return outstring
    @cherrypy.expose
    def right_hand(self, *args, **kwargs):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////


    // 利用函式呼叫組立右手 ARM, 組立增量次序為 1
    axis_plane_assembly(session, assembly, transf, 40, 0, 
                                  "LEGO_ARM_RT.prt", "A_13", "DTM1", "A_4", "DTM1");
                                  
      // 利用函式呼叫組立右手 HAND, 組立增量次序為 3
    axis_plane_assembly(session, assembly, transf, 40,6, 
                                  "LEGO_HAND.prt", "A_2", "DTM2", "A_1", "DTM3");
    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
        return outstring
    @cherrypy.expose
    def right_leg (self, *args, **kwargs):
        outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////



    // 右腳
    axis_plane_assembly(session, assembly, transf, 40, 1, 
                                  "LEGO_LEG_RT.prt", "A_8", "DTM4", "A_10", "DTM1");


    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
        return outstring
    @cherrypy.expose
    def left_leg(self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////




    /// 左腳
    axis_plane_assembly(session, assembly, transf, 40, 4, 
                                  "LEGO_LEG_LT.prt", "A_8", "DTM5", "A_10", "DTM1");
                                  
                                   
    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
            return outstring
    @cherrypy.expose
    def head(self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////




    // HEAD 則直接呼叫檔案名稱, 以 A_2, DTM2 約束
    axis_plane_assembly(session, assembly, transf, 40, 0, 
                                  "LEGO_HEAD.prt", "A_2", "DTM3", "A_2", "DTM2");
                                   
    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
            return outstring
    @cherrypy.expose
    def waist(self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////



    // WAIST 組立面為 DTM1, DTM2, DTM3, 組立增量次序為 6, 與 body 採三面 mate 組立
    three_plane_assembly2(session, assembly, transf, 40, 0, "LEGO_WAIST.prt", "DTM4", "DTM5", "DTM6", "DTM1", "DTM2", "DTM3"); 
                                   
    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
            return outstring
    @cherrypy.expose
    def hat(self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////



    // 紅帽
    axis_plane_assembly(session, assembly, transf, 40, 3, 
                                  "LEGO_HAT.prt", "A_2", "TOP", "A_2", "FRONT"); 
                                  
    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    <a href="index">返回首頁</a><br />
    </html>
    '''
            return outstring
    @cherrypy.expose
    def all(self, *args, **kwargs):
            outstring = '''
    <!DOCTYPE html> 
    <html>
    <head>
    <meta http-equiv="content-type" content="text/html;charset=utf-8">
    <script type="text/javascript" src="/static/weblink/examples/jscript/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/pfcUtils.js"></script>
    <script type="text/javascript" src="/static/weblink/wl_header.js"></script>
    </head>
    <body>
    </script><script language="JavaScript">
    /*man2.py 完全利用函式呼叫進行組立*/
    /*設計一個零件組立函式*/
    // featID 為組立件第一個組立零件的編號
    // inc 則為 part1 的組立順序編號, 第一個入組立檔編號為 featID+0
    // part2 為外加的零件名稱
    ////////////////////////////////////////////////
    // axis_plane_assembly 組立函式
    ////////////////////////////////////////////////
    function axis_plane_assembly(session, assembly, transf, featID, inc, part2, axis1, plane1, axis2, plane2){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    ids.Append(featID+inc);
    var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
    subassembly = subPath.Leaf;
    var asmDatums = new Array(axis1, plane1);
    var compDatums = new Array(axis2, plane2);
    var relation = new Array (pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN, pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
    var relationItem = new Array(pfcCreate("pfcModelItemType").ITEM_AXIS, pfcCreate("pfcModelItemType").ITEM_SURFACE);
    var constrs = pfcCreate("pfcComponentConstraints");
        for (var i = 0; i < 2; i++)
        {
            var asmItem = subassembly.GetItemByName (relationItem[i], asmDatums [i]);
            if (asmItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var compItem = componentModel.GetItemByName (relationItem[i], compDatums [i]);
            if (compItem == void null)
            {
                interactFlag = true;
                continue;
            }
            var MpfcSelect = pfcCreate ("MpfcSelect");
            var asmSel = MpfcSelect.CreateModelItemSelection (asmItem, subPath);
            var compSel = MpfcSelect.CreateModelItemSelection (compItem, void null);
            var constr = pfcCreate("pfcComponentConstraint").Create (relation[i]);
            constr.AssemblyReference  = asmSel;
            constr.ComponentReference = compSel;
            constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (true, false);
            constrs.Append(constr);
        }
    asmcomp.SetConstraints(constrs, void null);
    }
    // 以上為 axis_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly 採 align 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_ALIGN);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly() 函式
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    // three_plane_assembly2 採 mate 組立, 若 featID 為 0 表示為空組立檔案
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////
    function three_plane_assembly2(session, assembly, transf, featID, inc, part2, plane1, plane2, plane3, plane4, plane5, plane6){
    var descr = pfcCreate("pfcModelDescriptor").CreateFromFileName ("v:/home/lego/man/"+part2);
    var componentModel = session.GetModelFromDescr(descr);
    var componentModel = session.RetrieveModel(descr);
    if (componentModel != void null)
    {
        var asmcomp = assembly.AssembleComponent (componentModel, transf);
    }
    var ids = pfcCreate("intseq");
    // 若 featID 為 0 表示為空組立檔案
    if (featID != 0){
        ids.Append(featID+inc);
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = subPath.Leaf;
        }else{
        var subPath = pfcCreate("MpfcAssembly").CreateComponentPath(assembly, ids);
        subassembly = assembly;
        // 設法取得第一個組立零件 first_featID
        // 取得 assembly 項下的元件 id, 因為只有一個零件, 採用 index 0 取出其 featID
        var components = assembly.ListFeaturesByType(true, pfcCreate ("pfcFeatureType").FEATTYPE_COMPONENT);
        // 此一 featID 為組立件中的第一個零件編號, 也就是樂高人偶的 body
        var first_featID = components.Item(0).Id;
        }
    var constrs = pfcCreate("pfcComponentConstraints");
    var asmDatums = new Array(plane1, plane2, plane3);
    var compDatums = new Array(plane4, plane5, plane6);
    var MpfcSelect = pfcCreate("MpfcSelect");
    for (var i = 0; i < 3; i++)
    {
        var asmItem = subassembly.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, asmDatums[i]);
        
        if (asmItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var compItem = componentModel.GetItemByName(pfcCreate("pfcModelItemType").ITEM_SURFACE, compDatums[i]);
        if (compItem == void null)
        {
            interactFlag = true;
            continue;
        }
        var asmSel = MpfcSelect.CreateModelItemSelection(asmItem, subPath);
        var compSel = MpfcSelect.CreateModelItemSelection(compItem, void null);
        var constr = pfcCreate("pfcComponentConstraint").Create(pfcCreate("pfcComponentConstraintType").ASM_CONSTRAINT_MATE);
        constr.AssemblyReference = asmSel;
        constr.ComponentReference = compSel;
        constr.Attributes = pfcCreate("pfcConstraintAttributes").Create (false, false);
        constrs.Append(constr);
    }
    asmcomp.SetConstraints(constrs, void null);
    // 若 featID = 0 則傳回 first_featID
    if (featID == 0)
        return first_featID;
    }
    // 以上為 three_plane_assembly2() 函式, 主要採三面 MATE 組立
    //
    // 假如 Creo 所在的操作系統不是 Windows 環境
    if (!pfcIsWindows())
    // 則啟動對應的 UniversalXPConnect 執行權限 (等同 Windows 下的 ActiveX)
    netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
    // pfcGetProESession() 是位於 pfcUtils.js 中的函式, 確定此 JavaScript 是在嵌入式瀏覽器中執行
    var session = pfcGetProESession();
    // 設定 config option, 不要使用元件組立流程中內建的假設約束條件
    session.SetConfigOption("comp_placement_assumptions","no");
    // 建立擺放零件的位置矩陣, Pro/Web.Link 中的變數無法直接建立, 必須透過 pfcCreate() 建立
    var identityMatrix = pfcCreate("pfcMatrix3D");
    // 建立 identity 位置矩陣
    for (var x = 0; x < 4; x++)
    for (var y = 0; y < 4; y++)
    {
        if (x == y)
            identityMatrix.Set(x, y, 1.0);
        else
            identityMatrix.Set(x, y, 0.0);
    }
    // 利用 identityMatrix 建立 transf 座標轉換矩陣
    var transf = pfcCreate("pfcTransform3D").Create(identityMatrix);
    // 取得目前的工作目錄
    var currentDir = session.getCurrentDirectory();
    // 以目前已開檔的空白組立檔案, 作為 model
    var model = session.CurrentModel;
    // 查驗有無 model, 或 model 類別是否為組立件, 若不符合條件則丟出錯誤訊息
    if (model == void null || model.Type != pfcCreate("pfcModelType").MDL_ASSEMBLY)
    throw new Error (0, "Current model is not an assembly.");
    // 將此模型設為組立物件
    var assembly = model;

    /////////////////////////////////////////////////////////////////
    // 開始執行組立, 全部採函式呼叫組立
    /////////////////////////////////////////////////////////////////

    // Body 與空組立檔案採三個平面約束組立
    // 空組立面為 ASM_TOP, ASM_FRONT, ASM_RIGHT
    // Body 組立面為 TOP, FRONT, RIGHT
    // 若 featID=0 表示為空組立檔案, 而且函式會傳回第一個組立件的 featID
    var featID = three_plane_assembly(session, assembly, transf, 0, 0, "LEGO_BODY.prt", "ASM_TOP", "ASM_FRONT", "ASM_RIGHT", "TOP", "FRONT", "RIGHT"); 
    // 利用函式呼叫組立右手 ARM, 組立增量次序為 1
    axis_plane_assembly(session, assembly, transf, featID, 0, 
                                  "LEGO_ARM_RT.prt", "A_13", "DTM1", "A_4", "DTM1");
    // 利用函式呼叫組立左手 ARM, 組立增量次序為 2
    axis_plane_assembly(session, assembly, transf, featID, 0, 
                                  "LEGO_ARM_LT.prt", "A_9", "DTM2", "A_4", "DTM1");
    // 利用函式呼叫組立右手 HAND, 組立增量次序為 3
    axis_plane_assembly(session, assembly, transf, featID, 1, 
                                  "LEGO_HAND.prt", "A_2", "DTM2", "A_1", "DTM3");
    // 利用函式呼叫組立左手 HAND, 組立增量次序為 4
    axis_plane_assembly(session, assembly, transf, featID, 2, 
                                  "LEGO_HAND.prt", "A_2", "DTM2", "A_1", "DTM3");
    // 利用函式呼叫組立人偶頭部 HEAD, 組立增量次序為 5
    // BODY id 為 featID+0, 以 A_2 及  DTM3 約束
    // HEAD 則直接呼叫檔案名稱, 以 A_2, DTM2 約束
    axis_plane_assembly(session, assembly, transf, featID, 0, 
                                  "LEGO_HEAD.prt", "A_2", "DTM3", "A_2", "DTM2");
    // Body 與 WAIST 採三個平面約束組立
    // Body 組立面為 DTM4, DTM5, DTM6
    // WAIST 組立面為 DTM1, DTM2, DTM3, 組立增量次序為 6, 與 body 採三面 mate 組立
    three_plane_assembly2(session, assembly, transf, featID, 0, "LEGO_WAIST.prt", "DTM4", "DTM5", "DTM6", "DTM1", "DTM2", "DTM3"); 
    // 右腳
    axis_plane_assembly(session, assembly, transf, featID, 6, 
                                  "LEGO_LEG_RT.prt", "A_8", "DTM4", "A_10", "DTM1");
    // 左腳
    axis_plane_assembly(session, assembly, transf, featID, 6, 
                                  "LEGO_LEG_LT.prt", "A_8", "DTM5", "A_10", "DTM1");
    // 紅帽
    axis_plane_assembly(session, assembly, transf, featID, 5, 
                                  "LEGO_HAT.prt", "A_2", "TOP", "A_2", "FRONT"); 
    // regenerate 並且 repaint 組立檔案
    assembly.Regenerate (void null);
    session.GetModelWindow (assembly).Repaint();    
    </script>
    </body>
    </html>
    '''
            return outstring
class Download:
    @cherrypy.expose
    def index(self, filepath):
        return serve_file(filepath, "application/x-download", "attachment")
################# (4) 程式啟動區
# 配合程式檔案所在目錄設定靜態目錄或靜態檔案
application_conf = {'/static':{
        'tools.staticdir.on': True,
        # 程式執行目錄下, 必須自行建立 static 目錄
        'tools.staticdir.dir': _curdir+"/static"},
        '/downloads':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/downloads"},
        '/images':{
        'tools.staticdir.on': True,
        'tools.staticdir.dir': data_dir+"/images"}
    }
    
root = Midterm()
root.download = Download()
root.man = man.MAN()
root.man2 = man2.MAN()

#root.gear = gear.Gear()

if 'OPENSHIFT_REPO_DIR' in os.environ.keys():
    # 表示在 OpenSfhit 執行
    application = cherrypy.Application(root, config=application_conf)
else:
    # 表示在近端執行
    cherrypy.quickstart(root, config=application_conf)
