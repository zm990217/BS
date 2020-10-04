import axios from 'axios'
export const designOpera=data=>{
    return axios.post('/api/design',data).then(res=>res.data);
};

export const answerOpera=data=>{
    return axios.post('/api/answer',data).then(res=>res.data);
};
