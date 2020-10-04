<template lang="html">
    <div class="bg">
        <div class="register">
            <div class="title">注 册</div>
            <el-row>
                <el-form ref="registerForm" status-icon :model="registerForm" :rules="rules" label-width="100px" size="medium">
                    <el-form-item label="用户名" prop="username">
                        <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.username" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="邮箱" prop="email">
                        <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.email" placeholder="请输入邮箱"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="pass">
                        <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.pass" autocomplete="off" placeholder="请输入密码(不少于6位)" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="checkPass">
                        <el-input @keyup.enter.native="Register('registerForm')" v-model="registerForm.checkPass" autocomplete="off" placeholder="请再次输入密码" show-password></el-input>
                    </el-form-item>
                    <el-form-item style="margin-left: -25%">
                        <el-button type="primary" @click="Register('registerForm')" round>注 册</el-button>
                        <el-button @click="resetForm('registerForm')" style="margin-right: -5%" round>重 置</el-button>
                    </el-form-item>
                </el-form>
            </el-row>
            <div class="link">
                <el-link type="primary" href="/login">立即登录</el-link>
            </div>
        </div>
    </div>
</template>
<script>
    import { designOpera } from './api';
    export default {
        name: "Register",
        data(){
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                }
                else {
                    if (this.registerForm.checkPasswd !== '') {
                        this.$refs.registerForm.validateField('checkPass');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } 
                else if (value !== this.registerForm.pass) {
                    callback(new Error('两次输入密码不一致!'));
                }
                else {
                    callback();
                }
            };
            return{
                registerForm:{
                    username:'',
                    email:'',
                    pass:'',
                    checkPass:''
                },
                rules:{
                    username:[
                        { required: true, message: '账号不能为空', trigger: 'blur'},
                        { max: 20, message: '账号长度最长20位', trigger: 'blur' },
                        { min: 3, message: "账号长度最低3位", trigger: 'blur'}
                    ],
                    email:[
                        { required: true, message: '请输入邮箱地址', trigger: 'blur'},
                        { type: 'email', message: '请输入正确的邮箱', trigger: 'blur'},
                    ],
                    pass:[
                        { required: true, validator: validatePass, trigger:'blur'},
                        { min: 6, message: "密码长度最低6位", trigger: 'blur'}
                    ],
                    checkPass:[
                        { required: true, validator: validatePass2, trigger: 'blur' }
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
                    this.$router.push({path:'/home'})
                }
                else{
                    this.isLogin=false;
                    this.username='';
                }
            },
            Register(formName){
                this.$refs[formName].validate((valid)=>{
                    if(valid){
                        designOpera({
                            opera_type:'register',
                            username:this.registerForm.username,
                            password:this.$md5(this.registerForm.pass),
                            email:this.registerForm.email,
                        })
                        .then(data =>{
                            if(data.code==0){
                                this.$notify({
                                    type:'success',
                                    message:'注册成功，请登录'
                                }),
                                this.$router.push({path:'/login'});
                            }
                            else{
                                this.$message({
                                    type: 'error',
                                    message: '该用户名或邮箱已被注册'
                                });
                            }
                        })
                    }
                    else{
                        console.log('error submit!');
                        return false;
                    }
                })
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
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
.register {
    position: absolute;
    left:48%;
    top:40%;
    width:350px;
    height:320px;
    margin:-150px 0 0 -190px;
    padding:40px;
    border-radius: 5px;
    background: rgba(227, 221, 221, 0.51);
}
.el-form {
    padding-top: 5%;
    padding-right: 10%;
}
.el-form-item{
    margin-left: -10%;
}
.el-row {
    height: 100%;
    width: 100%;
}
.link{
    margin-top: -7%;
    text-align: center;
    margin-left: -5%;
}
.el-link{
    margin-left: 12px;
    line-height: 20px;
    font-size: 16px;
    color: black;
}
</style>>