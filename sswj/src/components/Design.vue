<template>
    <div class="Design">
        <h3>{{title}}</h3>
        <div v-if="desc!=''">{{desc}}</div>
        <el-card class="box-card" v-for="(item,index) in questionList" :key="item">
            <div slot="header" class="clearfix">
                <span style="color: red">
                    <span v-if="item.must==1">*</span>
                    <span v-else>&nbsp;</span>
                </span>
                <span>{{(index+1)+"."}}</span>
                {{item.title}}
                <span v-if="item.casc!=''" style="color: black;margin-left: 50px">此题目和&nbsp;&nbsp;{{item.cascQuestion}}&nbsp;&nbsp;的&nbsp;&nbsp;{{item.cascOption}}&nbsp;&nbsp;选项关联</span>
                <div style="float: right">
                    <el-button style="padding: 3px" type="primary" @click="editQuestion(item)" round>编辑题目</el-button>
                    <el-button style="padding: 3px" type="danger" @click="deleteQusetion(item.id)" round>删除题目</el-button>
                </div>
            </div>
            <div class="text item"  v-for="(option,index) in item.options" :key="index">
                <el-radio v-if="item.type=='radio'" v-model="item.radioValue" :label="index" style="margin: 5px;">{{ option.title }}</el-radio>
            </div>
            <el-checkbox-group v-if="item.type=='checkbox'" v-model="item.checkboxValue">
                <div class="text item"  v-for="(option,index) in item.options" :key="index">
                    <el-checkbox :label="index" style="margin: 5px;">{{ option.title }}</el-checkbox>
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
                resize="none"
                onkeypress="return(/[\d]/.test(String.fromCharCode(event.keyCode)))">
            </el-input>
            <el-radio-group v-model="item.scoreValue" v-for="(option,index) in item.options" :key="index">
                <div v-if="item.type=='score'">
                    <el-radio :label="index" style="margin: 5px">{{option.title}}</el-radio>
                </div>
            </el-radio-group>
        </el-card>
        <el-container>
            <el-footer>
                <el-row>
                    <el-button type="primary" plain @click="addQuestion(1)">单选题</el-button>
                    <el-button type="primary" plain @click="addQuestion(2)">多选题</el-button>
                    <el-button type="primary" plain @click="addQuestion(3)">问答题</el-button>
                    <el-button type="primary" plain @click="addQuestion(4)">评分题</el-button>
                    <el-button type="primary" plain @click="addQuestion(5)">数字题</el-button>
                </el-row>
            </el-footer>
        </el-container>

        <el-dialog :title="dialogTitle" :visible.sync="dialogShow" :close-on-click-modal="false" class="dialog">
            <el-form ref="form" :model="willAddQuestion" label-width="100px">
                <el-form-item label="是否必填" style="width: 100%;">
                    <el-checkbox v-model="willAddQuestion.must">必填</el-checkbox>
                </el-form-item>
                <el-form-item label="题目标题" style="width: 100%;">
                    <el-input v-model="willAddQuestion.title" placeholder="请输入标题" ></el-input>
                </el-form-item>
                <template v-if="willAddQuestion.type=='radio'||willAddQuestion.type=='checkbox'||willAddQuestion.type=='score'" >
                    <el-form-item :label="'选项'+(index+1)" v-for="(item,index) in willAddQuestion.options" :key="item">
                        <el-row>
                            <el-col :span="16">
                                <el-input  v-model="item.title" placeholder="请输入选项名(请勿使用纯数字)" style="width: 90%;"></el-input>
                            </el-col>
                            <el-col :span="8">
                                <el-button type="danger" plain class="" @click="deleteOption(index)">删除选项</el-button>
                            </el-col>
                        </el-row>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" plain class="addOptionButton" @click="addOption">新增选项</el-button>
                    </el-form-item>
                </template>
                <template v-if="willAddQuestion.type=='text'">
                    <el-form-item label="答题区行数">
                        <el-input-number v-model="willAddQuestion.row" :min="1" :max="10"></el-input-number>
                    </el-form-item>
                </template>
                <template v-if="willAddQuestion.type=='number'">
                </template>
                <el-form-item label="关联选择" style="width: 50%">
                    <el-cascader
                        v-model="willAddQuestion.casc"
                        :options="optionsList">
                    </el-cascader>
                </el-form-item>
            </el-form>
            <div style="width: 100%;text-align: right">
                <el-button style="margin-left: 10px;" @click="dialogShow=false">取消</el-button>
                <el-button type="primary" style="margin-left: 10px;" @click="checkAddQuestion">完成</el-button>
            </div>
        </el-dialog>
    </div>
</template>
<script>
    import {designOpera} from './api'
    export default {
        data(){
            return{
                dialogShow:false,
                dialogTitle:'',
                questionList:[],
                optionsList:[],
                wjId:0,
                title:'',
                desc:'',
                endTime:'',
                permissions:'',
                willAddQuestion:{
                    id:0,
                    type:'',
                    title:'',
                    options:[
                        {
                            title:'选项1',
                            id:0
                        },
                        {
                            title:'选项2',
                            id:0
                        }
                    ],
                    row:1,
                    casc:'',
                    cascQuestion:'',
                    cascOption:'',
                    must:false,
                },
                allType:[
                    {
                        value:'radio',
                        label:'单选题',
                    },
                    {
                        value:'checkbox',
                        label:'多选题',
                    },
                    {
                        value:'text',
                        label:'问答题',
                    },
                    {
                        value:'score',
                        label:'评分题'
                    },
                    {
                        value:'number',
                        label:'数字题'
                    },
                ],
            }
        },
        methods:{
            init(wjId,title,desc){
                this.wjId=wjId;
                this.title=title;
                this.desc=desc;
                this.getQuestionList();
            },
            getQuestionList(){
                var temp = sessionStorage.getItem('username');
                this.questionList=[];
                designOpera({
                    opera_type:'get_question_list',
                    wjId:this.wjId,
                    username:temp,
                })
                .then(data=>{
                    this.questionList=data.detail;
                })
            },
            addQuestion(type){
                this.willAddQuestion={
                    id:0,
                    type:'',
                    title:'',
                    options:[
                        {
                            title:'选项1',
                            id:0
                        },
                        {
                            title:'选项2',
                            id:0
                        }
                    ],
                    row:1,
                    casc:'',
                    cascQuestion:'',
                    cascOption:'',
                    must:false,
                };
                if (type == 1){
                    this.dialogTitle='添加单选题';
                    this.willAddQuestion.type='radio';
                }
                else if (type == 2){
                    this.dialogTitle='添加多选题';
                    this.willAddQuestion.type='checkbox';
                }
                else if (type == 3){
                    this.dialogTitle='添加简答题';
                    this.willAddQuestion.type='text';
                }
                else if (type == 4){
                    this.dialogTitle='添加评分题';
                    this.willAddQuestion.type='score';
                }
                else{
                    this.dialogTitle='添加数字题';
                    this.willAddQuestion.type='number';
                }
                this.dialogShow=true;
                this.getOptionsList(this.willAddQuestion.id);
            },
            getOptionsList(quesId){
                var temp = sessionStorage.getItem('username');
                this.optionsList=[];
                designOpera({
                    opera_type:'get_options_list',
                    wjId:this.wjId,
                    questionId:quesId,
                    username:temp
                })
                .then(data=>{
                    this.optionsList=data.detail;
                })
            },
            addOption(){
                this.willAddQuestion.options.push({
                    title:'',
                    id:0
                })
            },
            deleteOption(index){
                this.willAddQuestion.options.splice(index,1);
            },
            checkAddQuestion(){
                var temp = sessionStorage.getItem('username');
                designOpera({
                    opera_type:'add_question',
                    username:temp,
                    wjId:this.wjId,
                    title:this.willAddQuestion.title,
                    type:this.willAddQuestion.type,
                    options:this.willAddQuestion.options,
                    row:this.willAddQuestion.row,
                    must:this.willAddQuestion.must,
                    casc:this.willAddQuestion.casc.toString(),
                    questionId:this.willAddQuestion.id
                })
                .then(data=>{
                    this.dialogShow=false;
                    if(data.code==0){
                        this.$message({
                            type:'success',
                            message:'题目添加成功'
                        })
                        this.getQuestionList();
                    }
                    else{
                        this.$message({
                            type:'error',
                            message:data.msg
                        })
                    }
                    this.willAddQuestion={
                        id:0,
                        type:'',
                        title:'',
                        options:[''],
                        row:1,
                        casc:'',
                        cascQuestion:'',
                        cascOption:'',
                        must:false,
                    }
                })
            },
            editQuestion(item){
                this.willAddQuestion=item;
                if (item.type == 'radio'){
                    this.dialogTitle='编辑单选题';
                }
                else if (item.type == 'checkbox'){
                    this.dialogTitle='编辑多选题';
                }
                else if (item.type == 'text'){
                    this.dialogTitle='编辑简答题';
                }
                else if (item.type == 'score'){
                    this.dialogTitle='编辑评分题';
                }
                else{
                    this.dialogTitle='编辑数字题';
                }
                this.dialogShow=true;
                this.getOptionsList(this.willAddQuestion.id);
            },
            deleteQusetion(questionId){
                designOpera({
                    opera_type:'delete_question',
                    questionId:questionId
                })
                .then(data=>{
                    if(data.code==0){
                        this.$message({
                            type:'success',
                            message:'题目删除成功'
                        })
                        this.getQuestionList();
                    }
                    else{
                        this.$message({
                            type:'error',
                            message:data.msg
                        })
                    }
                })
            },
        }
    }
</script>
<style scoped>
.el-footer {
    background-color: #f3effd;
    color:  #f3effd;
    text-align: center;
    line-height: 60px;
  }
</style>>