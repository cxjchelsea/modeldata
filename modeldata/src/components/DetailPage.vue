<!-- DetailPage.vue -->
<template>
  <div class="container">
    <div class="container-module">
      <h1>{{ $route.params.chineseName }}</h1>
      <div class="lineone">
        <h2>模型基本属性</h2>
        <div class="buttons">
            <button @click="modelDoc">模型文档</button>
            <button @click="modelDown">模型下载</button>
            <router-link to="/"><button @click="back2home">返回首页</button></router-link>
        </div>
      </div>
      <div class="attribute">
        <div v-if="tableOne">
          <table>
            <tr v-for="(value, key) in tableOne" :key="key">
              <td class="key">{{ key }}</td>
              <td class="value">{{ value }}</td>
            </tr>
          </table>
        </div>
        <div v-if="tableTwo">
          <table>
            <tr v-for="(value, key) in tableTwo" :key="key">
              <td class="key">{{ key }}</td>
              <td class="value">{{ value }}</td>
            </tr>
          </table>
        </div>
      </div>
      <div class="linetwo">
        <h2>参数描述</h2>
        <h3>入库时间：{{ inboundTime }}</h3>
      </div>
      <div class="parameter">
        <div v-if="tableThree">
          <table>
            <tr v-for="(value, key) in tableThree" :key="key">
              <td class="key">{{ key }}</td>
              <td class="value">{{ value }}</td>
            </tr>
          </table>
        </div>
        <div v-if="tableFour">
          <table>
            <tr v-for="(value, key) in tableFour" :key="key">
              <td class="key">{{ key }}</td>
              <td class="value">{{ value }}</td>
            </tr>
          </table>
        </div>
      </div>
      <div class="predict">
          <table>
              <td><textarea  v-model="inputData"></textarea></td>
              <td>{{ resp_data }}</td>
          </table>
          <button @click="sendData">模型计算</button>
        </div>
      <div>
        <el-dialog v-model="dialogVisible">
          <p>您可以使用Python脚本命令调用此模型：</p>
          <pre><code  ref="codeBlock" class="language-javascript">
            {{ generatedCode }}
          </code></pre>
          <el-button @click="copyCode">复制代码</el-button>
          <el-button @click="downDll">模型下载</el-button>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import { GET_TABLE_DATA } from '@/config'
import {GET_PDF} from '@/config'
import {GET_DLL} from '@/config'
import {PREDICT} from '@/config'
import {GENERATE_CODE} from '@/config'

export default {
  data() {
    return {
      tableOne:null,
      inputData: '',
      resp_data: null,
      result:null,
      dialogVisible: false,
      generatedCode: '',
    };
  },
  mounted() {
    // 在组件挂载后，从后端获取数据
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const chineseName = this.$route.params.chineseName;
        const response = await fetch(GET_TABLE_DATA, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ chineseName }),
        });

        if (!response.ok) {
          throw new Error('请求失败');
        }
        const jsonData = await response.json();
        this.tableOne = jsonData.tableOne,
        this.tableTwo = jsonData.tableTwo,
        this.tableThree = jsonData.tableThree,
        this.tableFour = jsonData.tableFour,
        this.inboundTime = jsonData.inboundTime,
        this.inputData = jsonData.testCode;
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async sendData() {
      try {
        const inputData = this.inputData;
        const response = await fetch(PREDICT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ inputData }),
        });

        if (!response.ok) {
          throw new Error('请求失败');
        }
        const jsonData = await response.json();
        this.resp_data = jsonData[0]
      } catch (error) {
        console.error('Error:', error);
      }
    },
    async modelDoc() {
      try {
        const chineseName = this.$route.params.chineseName;
        const response = await fetch(GET_PDF, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error('请求失败');
        }
         
        const blob = await response.blob();
        // 创建一个新的 Blob URL，并在新窗口中打开该 URL
        const url = window.URL.createObjectURL(blob);
        window.open(url, '_blank', 'noopener,noreferrer');


    } catch (error) {
        console.error('Error generating PDF:', error);
    }
    },
    async modelDown() {
        this.dialogVisible = true;
        await this.fetchGenerateCode();
    },
    async fetchGenerateCode() {
      fetch(GENERATE_CODE, {
            method: 'GET',
            headers: {
            'Content-Type': 'application/json'
          },

          })
          .then(response => response.json())
          .then(data => {
            console.log('文本模板传回成功', data);
            this.generatedCode = data;
          })
          .catch(error => {
            console.error('传回失败', error);
          });
    },
    copyCode() {
      const codeBlock = this.$refs.codeBlock.textContent;
      const textarea = document.createElement('textarea');
      textarea.value = codeBlock;
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        this.$message({
          message: '代码已复制到剪贴板',
          type: 'success'
        });
      } catch (err) {
        this.$message({
          message: '复制失败',
          type: 'error'
        });
      }
      document.body.removeChild(textarea);
    },
    async downDll() {
      try {
        const response = await fetch(GET_DLL, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'dynamic library.dll';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error:', error);
      }
    },
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
.container{
  justify-content: center;
  display: flex;
}
.container-module{
  width:90%;
}
.lineone {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.attribute{
  display: flex;
}
.attribute table td.key {
  width: 200px;
  font-weight: bold;
}
.attribute table td.value {
  width: 427px;
}
.linetwo {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.parameter table td.key {
  width: 200px;
  font-weight: bold;
}
.parameter table td.value {
  width: 1088px;
}
.predict textarea {
  width: 650px;
  height:200px;
  font-size: 20px;
  border-color: transparent;
  white-space: pre-wrap;
  font-family: Arial;
}
.predict table {
  font-size: 20px;
}
.predict textarea:focus {
    outline: none; /* 去掉聚焦时的虚线边框 */
  }
.predict table td{
  width: 633px;
  height:200px;
}

.buttons {
  display: flex;
}
button {
  margin-left: 20px;
  margin-top:20px;
  border: none;
  background-color: #4caf50;
  color: #fff;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  width:150px;
}
table {
  border-collapse: collapse;
}
th, td {
  border: 1px solid #5b5b5b;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}
pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

code {
  font-family: "Courier New", Courier, monospace;
  color: #333;
}
</style>
