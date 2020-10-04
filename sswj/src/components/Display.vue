<template>
    <div class="display">
        <div class="content">
            <img src="/static/images/2.jpg" style="height: 232px; width: 800px">
            <h3>{{title}}</h3>
            <div v-if="desc!=''">{{desc}}</div>
            <div v-for="(item,index) in questionList" :key="item">
                <el-card class="box-card" v-if="showCheck(index)==true">
                    <div slot="header" class="clearfix">
                        <span style="color: red">
                            <span v-if="item.must==1">*</span>
                            <span v-else>&nbsp;</span>
                        </span>
                        <span>{{item.title}}</span>
                    </div>
                    <div class="text item"  v-for="option in item.options" :key="option">
                        <el-radio v-if="item.type=='radio'" v-model="item.radioValue" :label="option.id" style="margin: 5px;">{{ option.title }}</el-radio>
                    </div>
                    <el-checkbox-group v-if="item.type=='checkbox'" v-model="item.checkboxValue">
                        <div class="text item"  v-for="option in item.options" :key="option">
                            <el-checkbox :label="option.id" style="margin: 5px;">{{ option.title }}</el-checkbox>
                        </div>
                    </el-checkbox-group>
                    <el-input
                        v-if="item.type=='text'"
                        type="textarea"
                        :rows="item.row"
                        resize="none"
                        v-model="item.textValue">
                    </el-input>
                    <el-input
                        v-if="item.type=='number'"
                        type="textarea"
                        :rows="item.row"
                        v-model="item.numberValue"
                        resize="none">
                    </el-input>
                    <el-radio-group v-model="item.scoreValue" v-for="option in item.options" :key="option">
                        <div v-if="item.type=='score'">
                            <el-radio :label="option.id" style="margin: 5px">{{option.title}}</el-radio>
                        </div>
                    </el-radio-group>
                </el-card>
            </div>
            <el-button v-if="number!=0" type="primary" style="margin: 5px;" @click="submit">提交</el-button>
            <div class="bottom">
                <h3 v-if="number!=-1">剩余提交次数：{{number}}</h3>
            </div>
        </div>
    </div>
</template>
<script>
    import {answerOpera} from './api'
    export default {
        data(){
            return{
                wjId:0,
                isLogin:false,
                title:'',
                desc:'',
                questionList:[],
                permissions:'',
                number:'',
                startTimestamp:0,
            }
        },
        mounted(){
            this.wjId = this.$route.params.id;
            var temp = sessionStorage.getItem('username');
            answerOpera({
                opera_type:'get_info',
                wjId:this.wjId,
                username:temp
            })
            .then(data=>{
                if(data.code==0){
                    this.title=data.title;
                    this.desc=data.desc;
                    this.questionList=data.detail;
                    this.number=data.number;
                    this.permissions=data.permissions;
                }
                if(this.permissions == 'timeUser' || this.permissions == 'onlyUser' ){
                    this.state();
                };
                this.startTimestamp=new Date().getTime();
            })   
        },
        methods:{
            state(){
                var temp = sessionStorage.getItem('username');
                console.log(temp);
                if(temp!=null && temp!='None'){
                    this.isLogin=true;
                    this.username=temp;
                }
                else{
                    this.isLogin=false;
                    this.username='';
                    this.$router.push({path:'/login'})
                }
            },
            showCheck(index){
                var i;
                var _this = this;
                if(_this.questionList[index].casc!=''){
                    for(i=0;i<_this.questionList.length;i++){
                        if (_this.questionList[i].id==_this.questionList[index].casc_questionId){
                            if(_this.questionList[i].radioValue==_this.questionList[index].casc_optionId){
                                return true;
                            }
                            else return false;
                        }
                    }
                }
                else return true;
            },  
            submit(){
                let useTime=parseInt((new Date().getTime()-this.startTimestamp)/1000);
                answerOpera({
                    opera_type:'submit_wj',
                    wjId:this.wjId,
                    useTime:useTime,
                    detail:this.questionList,
                    number:this.number
                })
                .then(data=>{
                    if(data.code==0){
                        this.$router.push({path:'/thankyou'});
                    }
                    else{
                        this.$message({
                            type:'error',
                            message:data.msg
                        })
                    }
                })
            },
        },
    }
</script>
<style scoped>
.display{
    text-align: center;
    padding: 20px;
    background: #f3effd;
}
.display .content{
    width: 100%;
    max-width: 800px;
    display: inline-block;
    text-align: center;
}
.display .box-card{
    text-align: left;
    width: 100%;
    margin:10px 0 10px 0;
}
.display .bottom{
    margin: 20px 10px 20px 10px;
    color: #909399;
}
.display a:link,a:visited,a:active {
    color: #909399;
    text-decoration:none;
}
</style>>