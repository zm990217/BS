<template lang="html">
    <div class = "home">
        <el-container style="height: 100%; border: 1px solid #eee">
            <el-aside width="200px" style="background-color: #545c64">
                <el-menu
                    default-active = "1"
                    class = "el-menu-vertical-demo"
                    background-color = "#545c64"
                    text-color = "#fff"
                    active-text-color = "fffd04b">
                    <el-menu-item index="quesetionList" @click="goHome">
                        <i class="el-icon-document"></i>
                        <span slot="title">问卷列表</span>
                    </el-menu-item>
                    <el-menu-item index="addQuestion" @click="addWjButtonClick">
                        <i class="el-icon-circle-plus-outline"></i>
                        <span slot="title">添加问卷</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <div v-show="showList==true">
                <el-button @click="clearFilter">清除问卷过滤器</el-button>
                <el-table 
                    ref="WjList" 
                    :data="wjList" 
                    border
                    style="width:100%" 
                    stripe>
                    <el-table-column
                        prop="id"
                        label="问卷编号"
                        width="120">
                    </el-table-column>
                    <el-table-column 
                        prop="title" 
                        label="问卷标题" 
                        width="120">
                    </el-table-column>
                    <el-table-column 
                        prop="status" 
                        label="问卷状态" 
                        width="100" 
                        :filters="[{text:'未发布',value:'未发布'},{text:'已发布',value:'已发布'}]"
                        :filter-method="filterStatus" 
                        filter-pacement="bottom-end">
                        <div slot-scope="scope">
                            <el-tag :type="scope.row.status === '未发布'?'primary':'success'" disable-transitions>{{scope.row.status}}</el-tag>
                        </div>
                    </el-table-column>
                    <el-table-column 
                        prop="endTime" 
                        label="截止时间" 
                        width="180">
                    </el-table-column>
                    <el-table-column 
                        prop="permissions" 
                        label="问卷权限" 
                        width="180">
                    </el-table-column>
                    <el-table-column 
                        prop="desc" 
                        label="问卷描述" 
                        width="240">
                    </el-table-column>
                    <el-table-column prop="op" label="操作" width="340" fixed="right">
                        <div slot-scope="scope">
                            <el-tooltip class="item" effect="dark" content="编辑问卷" placement="bottom">
                                <el-button icon="el-icon-edit" type="primary" class="rightButton" @click="designWj(scope.row)" circle size="mini"></el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" content="问卷信息" placement="bottom">
                                <el-button icon="el-icon-setting" type="primary" class="rightButton" @click="editWjInfo(scope.row)" circle size="mini"></el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" :content="scope.row.status==='未发布'?'发布问卷':'暂停问卷'" placement="bottom" >
                                <el-button :icon="scope.row.status==='未发布'?'el-icon-video-play':'el-icon-video-pause'"  :type="scope.row.status==='未发布'?'success':'warning'" class="rightButton" @click="pushWj(scope.row.id,scope.row.status)" circle size="mini"></el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" content="删除问卷" placement="bottom">   
                                <el-button icon="el-icon-delete" type="danger" class="rightButton" @click="deleteWj(scope.row.id)" circle size="mini"></el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" content="预览问卷" placement="bottom">
                                <el-button icon="el-icon-view" type="info" class="rightButton" @click="previewWj(scope.row.id)" circle size="mini"></el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" content="分享问卷" placement="bottom">
                                <el-button icon="el-icon-share" type="info" class="rightButton" @click="shareWj(scope.row.id)" circle size="mini"></el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" content="问卷统计" placement="bottom">
                                <el-button icon="el-icon-data-analysis" type="primary" class="rightButton" @click="dataShow(scope.row)" circle size="mini"></el-button>
                            </el-tooltip>
                        </div>
                    </el-table-column>
                </el-table>
                </div>
                <design ref="design" v-show="showWj==true"></design>
                <data-show ref="datashow" v-show="showData==true"></data-show>
            </el-main>
        </el-container>
        <el-dialog :title="dialogTitle" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
            <el-form ref="form" :model="willAddWj" label-width="80px">
                <el-form-item label="问卷标题" style="width: 100%;" required>
                    <el-input v-model="willAddWj.title" placeholder="请输入问卷标题" ></el-input>
                </el-form-item>
                <el-form-item label="问卷描述" style="width: 100%;">
                    <el-input v-model="willAddWj.desc" type="textarea" placeholder="请输入问卷描述" rows="2"></el-input>
                </el-form-item>
                <el-form-item label="问卷权限" style="width: 100%;">
                    <el-select v-model="willAddWj.permissions" placeholder="请选择问卷权限" @change="typeChange">
                        <el-option
                            v-for="item in perm"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="截止时间" style="width: 100%">
                    <el-date-picker
                        v-model="willAddWj.endTime"
                        type="datetime"
                        placeholder="请选择截止时间"
                        default-time="23:59:59"
                        value-format="yyyy-MM-dd HH:mm:ss">
                    </el-date-picker>
                </el-form-item>
            </el-form>
            <div style="width: 100%;text-align: right">
                <el-button style="margin-left: 10px;" @click="dialogShow=false">取消</el-button>
                <el-button type="primary" style="margin-left: 10px;" @click="addWj">确定</el-button>
            </div>
        </el-dialog>
        <el-dialog
            title="问卷链接"
            :visible.sync="dialogVisible"
            width="30%"
            :before-close="handleClose">
            <span>{{url}}</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>
<script>
    import {designOpera} from './api'
    import Design from './Design.vue'
    import DataShow from './DataShow.vue'
    import ElButton from "../../node_modules/element-ui/packages/button/src/button";
    import QRCode from 'qrcode'
    export default {
        components:{
            ElButton,
            Design,
            QRCode,
            DataShow,
        },
        data(){
            return{
                wjList:[],
                loading:false,
                dialogShow:false,
                dialogTitle:'添加问卷',
                shareDialogShow:false,
                dialogVisible:false,
                showList:true,
                showWj:false,
                showData:false,
                url:'',
                willAddWj:{
                    id:0,
                    title:'',
                    desc:'感谢您能抽时间参与本次问卷！',
                    endTime:'',
                    permissions:''
                },
                selectWj:{

                },
                shareInfo:{
                    url:''
                },
                perm:[
                    {
                        value:'allPrem',
                        label:'不限制',
                    },
                    {
                        value:'onlyUser',
                        label:'仅限注册用户',
                    },
                    {
                        value:'timeUser',
                        label:'仅限注册用户且最多填写3次',
                    },
                    {
                        value:'timeAll',
                        label:'不限制用户但最多3次'
                    }
                ],
            }
        },
        mounted(){
            this.state();
        },
        methods:{
            state(){
                var temp = sessionStorage.getItem('username');
                if(temp!=null){
                    this.isLogin=true;
                    this.username=temp;
                    this.getWjList();
                }
                else{
                    this.isLogin=false;
                    this.username='';
                    this.$router.push({path:'/login'})
                }
            },
            getWjList(){
                this.showWj = false;
                this.showData = false;
                this.showList = true;
                this.loading=true;
                var temp = sessionStorage.getItem('username');
                designOpera({
                    opera_type:'get_wj_list',
                    username:temp
                })
                .then(data=>{
                    this.wjList=data.data.detail;
                    this.loading=false;
                })
            },
            goHome(){
                this.getWjList();
            },
            addWjButtonClick(){
                this.dialogTitle="添加问卷";
                this.dialogShow=true;
                this.willAddWj={
                    id:0,
                    title:'',
                    desc:'感谢您能抽时间参与本次问卷！',
                    endTime:'',
                    permissions:''
                };
            },
            addWj(){
                if (this.willAddWj.title == ''){
                    this.$message({
                        type: 'error',
                        message: '标题不能为空'
                    });
                    return;
                }
                var temp = sessionStorage.getItem('username');
                designOpera({
                    opera_type:'add_wj',
                    username:temp,
                    title:this.willAddWj.title,
                    id:this.willAddWj.id,
                    desc:this.willAddWj.desc,
                    endTime:this.willAddWj.endTime,
                    permissions:this.willAddWj.permissions
                })
                .then(data=>{
                    if(data.code==0){
                        this.$message({
                            type: 'success',
                            message: '保存成功!'
                        });
                        this.getWjList();
                    }
                    else{
                        this.$message({
                            type: 'error',
                            message: data.msg
                        });
                    }
                });
                this.dialogShow=false;
                this.willAddWj.title='';
            },
            designWj(row){
                this.showList = false;
                this.showData = false;
                this.showWj = true;
                this.$refs.design.init(row.id,row.title,row.desc);
            },
            editWjInfo(row){
                this.dialogTitle = "修改问卷信息"
                this.dialogShow = true;
                this.willAddWj = row;
            },
            pushWj(id,status){
                var newStatus = 0;
                if (status == "未发布"){
                    newStatus = 1;
                }
                else {
                    newStatus = 0;
                }
                designOpera({
                    opera_type:'push_wj',
                    wjId:id,
                    status:newStatus
                })
                .then(data=>{
                    if (data.code == 0){
                        this.$message({
                            type:'success',
                            message: data.status == 1 ? '发布成功' : '暂停成功'
                        });
                        this.getWjList();
                    }
                    else{
                        this.$message({
                            type:'error',
                            msg:data.msg
                        });
                    }
                })
            },
            previewWj(id){
                let url=window.location.origin+"/display/"+id;
                window.open(url);
            },
            deleteWj(id){
                this.$confirm('此操作将永久删除该问卷, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    var temp = sessionStorage.getItem('username');
                    designOpera({
                        opera_type:'delete_wj',
                        username:temp,
                        wjId:id
                    })
                    .then(data=>{
                        if (data.code == 0){
                            this.$message({
                                type:'success',
                                message:'删除成功'
                            });
                            this.getWjList();
                        }
                        else{
                            this.$message({
                                type:'error',
                                message:data.msg
                            });
                        }
                    })
                }).catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消删除'
                    });          
                });
            },
            shareWj(id){
                this.dialogVisible=true;
                this.url=window.location.origin+"/display/"+id;
            },
            handleClose(done) {
                this.$confirm('确认关闭？')
                .then(_ => {
                    done();
                })
                .catch(_ => {});
            },
            dataShow(row){
                this.showList = false;
                this.showWj = false;
                this.showData = true;
                this.$refs.datashow.init(row.id,row.title,row.desc);
            },
            clearFilter() {
                this.$refs.WjList.clearFilter();
            },
            filterStatus(value, row) {
                return row.status === value;
            },
            typeChange(value){
                this.willAddWj.permissions=value;
            },
        },
    }
</script>
<style scoped>
.home{
    position: absolute;
    width: 100%;
    height: calc(100vh - 100px);
    text-align: left;
    background: #f3effd;
}
</style>>