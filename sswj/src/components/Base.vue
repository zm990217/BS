<template lang="html">
    <div class="main">
        <el-container>
            <el-header>
                <div class="logo" @click="goto('/index')">
                    <img src="/static/images/logo3.png" class="logoImg">
                    <span style="color: #303133">三水问卷</span>
                </div>
                <div class="bar">
                    <template v-if="!isLogin">
                        <el-button type="primary" plain style="font-size: 15px;" @click="goto('/login')" round>登录</el-button>
                        <el-button type="primary" plain style="font-size: 15px;" @click="goto('/register')" round>注册</el-button>
                    </template>
                    <template v-else>
                        <el-dropdown trigger="click" @command="handleCommand">
                            <span class="el-dropdown-link">
                                <i class="el-icon-user"></i>{{username}}<i class="el-icon-arrow-down el-icon--right"></i>
                            </span>
                            <el-dropdown-menu slot="dropdown">
                                <el-dropdown-item command="a">问卷管理</el-dropdown-item>
                                <el-dropdown-item command="b">修改密码</el-dropdown-item>
                                <el-dropdown-item command="c" divided>退出登录</el-dropdown-item>
                            </el-dropdown-menu>
                        </el-dropdown>
                    </template>
                </div>
            </el-header>
            <el-main style="padding: 0">
                <router-view @state="state"/>
            </el-main>
        </el-container>
    </div>
</template>
<script>
    import {designOpera} from './api'
    export default {
        name:'Base',
        data: function(){
            return{
                isLogin: false,
                username:''
            }
        },
        methods:{
            state(){
                var temp = sessionStorage.getItem('username');
                if(temp!=null){
                    this.isLogin=true;
                    this.username=temp;
                }
                else{
                    this.isLogin=false;
                    this.username='';
                }
            },
            goto(a){
                this.$router.push({path:a});
            },
            handleCommand(command) {
                if(command=='a'){
                    this.goto('/home');
                }
                else if(command=='b'){
                    this.goto('/resetPasswd')
                }
                else{
                    sessionStorage.clear()
                    this.state()
                    this.goto('/login')
                }
            }

        },
        mounted(){
            this.state();
        }
    }
</script>

<style scoped>
.main{
    position: absolute;
    width: 100%;
    height: 100%;
    background: #b8d7e9;
}
.bar{
    float: right;
    margin-right: 50px;
    line-height: 60px;
}
.logo{
    height: 60px;
    display: inline-block;
    line-height: 60px;
    font-size: 20px;
    position: absolute;
    left: 100px;
    color: #303133;
    cursor: pointer;
}
.logoImg{
    width: 30px;
    vertical-align: middle;
}
.el-dropdown-link {
    cursor: pointer;
    color: #409EFF;
}
.el-icon-arrow-down {
    font-size: 12px;
}
</style>>