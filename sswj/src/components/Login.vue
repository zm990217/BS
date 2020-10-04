<template lang="html">
    <div class='bg'>
        <div class="login">
            <div class="title">登 录</div>
            <el-row type="flex" justify="center">
                <el-form ref="loginForm" :rules="rules" :model="loginForm">
                    <el-form-item prop="username">
                        <el-input @keyup.enter.native="login('loginForm')" v-model="loginForm.username" placeholder="请输入用户名"><i class="el-icon-user" slot="prefix"/></el-input>
                    </el-form-item>
                    <el-form-item prop="passwd">
                        <el-input @keyup.enter.native="login('loginForm')" v-model="loginForm.passwd" placeholder="请输入密码" show-password><i class="el-icon-lock" slot="prefix"/></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="login('loginForm')" round width="100%">登 录</el-button>
                    </el-form-item>
                </el-form>
            </el-row>
            <div class="link">
                <el-link type="primary" href="/register">立即注册</el-link>
            </div>
        </div>
    </div>
</template>

<script>
    import {designOpera} from './api'
    import {Loading} from 'element-ui';
    export default {
        name: 'Login',
        inject: ['reload'],
        data(){
            return{
                loginForm:{
                    username:'',
                    passwd:'',
                },
                rules:{
                    username: [
                        { required: true, message: '账号不能为空', trigger: 'blur'},
                        { max: 20, message: '账号长度最长20位', trigger: 'blur' },
                        { min: 3, message: "账号长度最低3位", trigger: 'blur'}
                    ], 
                    passwd: [
                        { required: true, message: '请输入密码', trigger:'blur'},
                        { min: 6, message: "密码长度最低6位", trigger: 'blur'}
                    ]
                }
            }
        },
        methods:{
            state(){
                var temp = sessionStorage.getItem('username');
                if(temp!=null){
                    this.isLogin=true;
                    this.username=temp;
                    this.$router.push({path:'/home'});
                }
                else{
                    this.isLogin=false;
                    this.username='';
                }
            },
            async login(formName){
                this.$refs[formName].validate(async (valid) =>{
                    if(valid){
                        designOpera({
                            opera_type:'login',
                            username:this.loginForm.username,
                            password:this.$md5(this.loginForm.passwd)
                        })
                        .then(data => {
                            if(data.code==0){
                                this.$notify({
                                    type:'success',
                                    message:this.loginForm.username+'，欢迎您登录三水问卷系统'
                                }),
                                this.$router.push({path:'/home'});
                                sessionStorage.setItem("username",this.loginForm.username)
                                this.$emit('state');
                            }
                            else{
                                this.$message({
                                    type: 'error',
                                    message: data.msg
                                });
                            }
                        })  
                    }
                    else{
                        return false;
                    }
                })
            }
        },
        mounted(){
            this.state();
        }
    }
</script>
<style scoped>
.bg{
    position: absolute;
    width:100%;
    height:100%;
    background-image: url("/static/images/27.jpg");
    background-repeat: no-repeat;
    background-size: auto 100% 100%;
}
.title {
    font-size: 24px; 
    font-weight: bolder; 
    margin-left: 5px;
    color:black;
}
.login {
    position: absolute;
    left:48%;
    top:40%;
    width:320px;
    height:250px;
    margin:-150px 0 0 -190px;
    padding:40px;
    border-radius: 5px;
    background: rgba(227, 221, 221, 0.51);
}
.el-form {
    padding-top: 5%;
    padding-left: 10%;
    padding-right: 10%;
    width:280px;
}
.el-row {
    height: 100%;
    width: 100%;
}
.link{
    margin-top: -13%;
    text-align: center;
    margin-left: -5%;
}
.el-link{
    margin-left: 12px;
    line-height: 20px;
    font-size: 16px;
    color: black;
}
</style>