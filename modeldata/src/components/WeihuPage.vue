<!-- WeihuPage.vue -->
<template>
  <div class="container">
    <div class="container-module">
      <div class="label">
        <table>
          <tr>
          <td v-for="model in labelList" :key="model">
            <el-radio  v-model="selectedLabel" :label="model" @change="fetchList">{{ model }}</el-radio>
          </td>
          <td>
            <button @click="sendModel">确定</button>
          </td>
        </tr>
        </table>
      </div>
      <div class="modelprocess">
        <div class="model">
          <table>
            <tr>
              <td>
                <input type="checkbox" v-model="chooseAll" @change="selectAllModels">全选
              </td>
            </tr>
            <tr v-for="model in modelList" :key="model">
              <td>
                <input type="checkbox" v-model="selectedModel" :value="model">{{ model }}
              </td>
            </tr>
          </table>
        </div>
        <div class="product">
          <el-dialog v-model="dialogVisible">
            <p>您确定要编辑以下模型数据吗？</p>
            <div class="table">
              <table>
                <thead>
                  <tr>
                    <th v-for="(key, index) in isAdmin ? keyAdmin : keyUser" :key="index">{{ key }}</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in modelData" :key="index">
                    <td>{{ item['模型名称（中文）'] }}</td>
                    <td><input type="text" v-model="item['所属产线']"></td>
                    <td><input type="text" v-model="item['所属工序']"></td>
                    <td v-if="isAdmin"><input type="datetime-local" v-model="item['入库时间']"></td>
                  </tr>
                </tbody>
              </table>
            </div>
            <button @click="sendEdit">确定</button>
            <button @click="cancelEdit">取消</button>
          </el-dialog>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import {SEND_LIST} from '@/config'
import {SEND_EDIT} from '@/config'
import {GET_MODEL_DATA} from '@/config'

export default {
  props: {
    isAdmin: Boolean,
  },
  data() {
    return {
      selectedLabel: '力能参数',
      labelList: [
        "力能参数", "负荷分配", "工艺温度", "三维变形", "微观组织", "力学性能",
      ],
      selectedModel:[],
      modelList:[],
      dialogVisible: false, 
      keyAdmin:['模型名称（中文）','所属产线','所属工序','入库时间'],
      keyUser:['模型名称（中文）','所属产线','所属工序'],
      modelData:[],
      chooseAll:false,
    };
  },
  created() {
    this.fetchList();
  },
  methods:{
    fetchList() {
      fetch(SEND_LIST, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedLabel: this.selectedLabel,
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log('所选标签传回成功', data);
          this.modelList = data.modelList;
        })
        .catch(error => {
          console.error('传回失败', error);
        });
    },
    selectAllModels() {
      if (this.chooseAll) {
        this.selectedModel = this.modelList.slice();
      } else {
        this.selectedModel = []; // 清空selectedModel
      }
    },
    sendModel() {
      this.dialogVisible = true; 
      this.fetchModel();
    },
    async fetchModel() {
      try {
        const response = await fetch(GET_MODEL_DATA, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ selectedModel: this.selectedModel, }),
        });

        if (!response.ok) {
          throw new Error('请求失败');
        }
        const jsonData = await response.json();
        this.modelData = jsonData.modelData
      } catch (error) {
        console.error('Error:', error);
      }
    },
    sendEdit() {
      fetch(SEND_EDIT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedModel: this.selectedModel,
          modelData:this.modelData
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log('所选标签编辑传回成功', data);
            this.dialogVisible = false; 
            this.selectedModel = []
          })
          .catch(error => {
            console.error('传回失败', error);
          });
    },
    cancelEdit() {
      this.dialogVisible = false;
    },
  },
};
</script>
<style>
.container{
  justify-content: center;
  display: flex;
}
.container-module{
  width:65%;
}
.modelprocess{
  display:flex;
}
.label table {
  border-collapse: collapse;
  width:800px;
}
.label th, td {
  border: 1px solid #5b5b5b;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}
.model table {
  border-collapse: collapse;
  width:800px;
}
.model th, td {
  border: 1px solid #5b5b5b;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}
.product {
  display: flex;
  flex-direction: column;
  align-items: center; /* 可以根据需要调整对齐方式 */
}
.product table {
  border-collapse: collapse;
  width:100%;
}
.product th, td {
  border: 1px solid #5b5b5b;
  padding: 8px;
  text-align: left;
  vertical-align: top;
}
</style>
