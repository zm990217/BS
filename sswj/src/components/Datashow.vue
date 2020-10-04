<template>
    <div class="Datashow">
        <h3>{{title}}</h3>
        <div v-if="desc!=''">{{desc}}</div>
        <el-card class="box-card" v-for="(item,index) in answerList" :key="index">
            <div slot="header" class="clearfix">
                <span>{{(index+1)+"."}}</span>
                {{item.title}}
            </div>
            <div v-if="item.type=='radio' || item.type=='checkbox' || item.type=='score'">
                <el-row>
                    <el-col :span="12">
                        <el-table
                            ref="countShow"
                            :data="item.countShow"
                            border
                            style="width:80%"
                            stripe>
                            <el-table-column
                                prop="optionTitle"
                                label="选项"
                                min-width="33%">
                            </el-table-column>
                            <el-table-column
                                prop="count"
                                label="数量"
                                min-width="33%">
                            </el-table-column>
                            <el-table-column
                                prop="per"
                                label="占比"
                                min-width="33%">
                            </el-table-column>
                        </el-table>
                    </el-col>
                    <el-col :span="12">
                        <div :id='"graph"+index' style="width: 300px;height: 200px">
                            <el-button type="primary" style="margin-left: 10px;" @click="graphShow(index)">查看统计图</el-button>
                        </div>
                    </el-col>
                </el-row>
            </div>
            <div v-if="item.type=='text'">
                <el-table
                    ref="textShow"
                    :data="item.answer"
                    style="80%"
                    stripe
                    >
                    <el-table-column
                        prop="content"
                        label="回答详情">
                    </el-table-column>
                </el-table>
            </div>
            <div v-if="item.type=='number'">
                <el-table
                    ref="numberShow"
                    :data="item.answer"
                    style="80%"
                    stripe
                    >
                    <el-table-column
                        prop="flag"
                        label="">
                    </el-table-column>
                    <el-table-column
                        prop="number"
                        label="数据">
                    </el-table-column>
                </el-table>
            </div>
        </el-card>
    </div>
</template>
<script>
    import echarts from 'echarts'
    import {designOpera} from './api'
    export default {
        data(){
            return{
                answerList:[],
                wjId:0,
                title:'',
                desc:''
            }
        },
        methods:{
            init(wjId,title,desc){
                this.wjId=wjId;
                this.title=title;
                this.desc=desc;
                this.getAnswerShow();
            },
            getAnswerShow(){
                var temp = sessionStorage.getItem('username');
                designOpera({
                    opera_type:'get_answer_list',
                    wjId:this.wjId,
                    username:temp,
                })
                .then(data=>{
                    console.log(data);
                    if(data.code==0){
                        this.answerList = data.detail;
                    }
                    else{
                        this.$message({
                            type:'error',
                            message:data.msg
                        })
                    }
                })
            },
            graphShow(index){
                var myChart = echarts.init(document.getElementById('graph'+index));
                var option = {
                    tooltip:{
                    },
                    legend:{
                        data:['数量']
                    },
                    dataset:{
                        dimensions:['optionTitle',"count","per"],
                        source:this.answerList[index].countShow
                    },
                    series:[{
                        name: '统计结果',
                        type: 'pie',
                        radius: '55%',
                        roseType: 'angle',
                        center: ['50%', '50%']
                    }]
                };
                myChart.setOption(option);
            }
        }
    }
</script>
<style scoped>
.el-table{
    margin: 0;
}
</style>>