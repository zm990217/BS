<template lang="html">
    <div class="bg">
        <div class="resetPasswd">
            <div class="title">修改密码</div>
            <el-row>
                <el-form ref="resetPasswdForm" status-icon :model="resetPasswdForm" :rules="rules" label-width="100px" size="medium">
                    <el-form-item label="用户名" prop="username">
                        <el-input @keyup.enter.native="resetPasswd('resetPasswdForm')" v-model="resetPasswdForm.username" placeholder="请输入用户名"></el-input>
                    </el-form-item>
                    <el-form-item label="原密码" prop="oldpass">
                        <el-input @keyup.enter.native="resetPasswd('resetPasswdForm')" v-model="resetPasswdForm.oldpass" autocomplete="off" placeholder="请输入原密码" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="新密码" prop="newpass">
                        <el-input @keyup.enter.native="resetPasswd('resetPasswdForm')" v-model="resetPasswdForm.newpass" autocomplete="off" placeholder="请输入新密码(不少于6位)" show-password></el-input>
                    </el-form-item>
                    <el-form-item label="确认新密码" prop="checkNewPass">
                        <el-input @keyup.enter.native="resetPasswd('resetPasswdForm')" v-model="resetPasswdForm.checkNewPass" autocomplete="off" placeholder="请再次输入新密码" show-password></el-input>
                    </el-form-item>
                    <el-form-item style="margin-left: -25%">
                        <el-button type="primary" @click="resetPasswd('resetPasswdForm')" round>提 交</el-button>
                        <el-button @click="resetForm('resetPasswdForm')" style="margin-right: -5%" round>重 置</el-button>
                    </el-form-item>
                </el-form>
            </el-row>
        </div>
    </div>
</template>
<script>
    import { designOpera } from './api';
    export default {
        name:'ResetPasswd',
        data(){
            var validatePass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入密码'));
                }
                else {
                    if (this.resetPasswdForm.checkNewPasswd !== '') {
                        this.$refs.resetPasswdForm.validateField('checkNewPass');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入密码'));
                } 
                else if (value !== this.resetPasswdForm.newpass) {
                    callback(new Error('两次输入密码不一致!'));
                }
                else {
                    callback();
                }
            };
            return{
                resetPasswdForm:{
                    username:'',
                    oldpass:'',
                    newpass:'',
                    checkNewPass:''
                },
                rules:{
                    username:[
                        { required: true, message: '账号不能为空', trigger: 'blur'},
                        { max: 20, message: '账号长度最长20位', trigger: 'blur' },
                        { min: 3, message: "账号长度最低3位", trigger: 'blur'}
                    ],
                    oldpass:[
                        { required: true, validator: validatePass, trigger:'blur'},
                        { min: 6, message: "密码长度最低6位", trigger: 'blur'}
                    ],
                    newpass:[
                        { required: true, validator: validatePass, trigger:'blur'},
                        { min: 6, message: "密码长度最低6位", trigger: 'blur'}
                    ],
                    checkNewPass:[
                        { required: true, validator: validatePass2, trigger: 'blur' }
                    ]
                }
            }
        },
        methods:{
            resetPasswd(formName){
                this.$refs[formName].validate((valid)=>{
                    if(valid){
                        designOpera({
                            opera_type:'resetPasswd',
                            username:this.resetPasswdForm.username,
                            oldpassword:this.$md5(this.resetPasswdForm.oldpass),
                            newpassword:this.$md5(this.resetPasswdForm.newpass)
                        })
                        .then(data =>{
                            if(data.code==0){
                                this.$notify({
                                    type:'success',
                                    message:'修改成功，请登录'
                                }),
                                sessionStorage.clear();
                                this.$router.push({path:'/login'});
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
                        console.log('error submit!');
                        return false;
                    }
                })
            },
        },
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
.resetPasswd {
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
</style>