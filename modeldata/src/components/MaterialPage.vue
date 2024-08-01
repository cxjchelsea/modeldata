<template>
  <div>
    <el-header>材料信息数据库</el-header>
    <div class="filters">
      <select v-model="selectedType" @change="sendselectedType">
        <option disabled value="">请选择类别</option>
        <option v-for="item in selectedTypeOptions" :value="item" :key="item">{{ item }}</option>
      </select>
      <select v-model="selectedType1" @change="sendselectedType1">
        <option disabled value="">请选择类别1</option>
        <option v-for="item in selectedType1Options" :value="item" :key="item">{{ item }}</option>
      </select>
      <select v-model="selectedType2" @change="sendselectedType2">
        <option disabled value="">请选择类别2</option>
        <option v-for="item in selectedType2Options" :value="item" :key="item">{{ item }}</option>
      </select>
      <select v-model="selectedGrade" @change="sendselectedGrade">
        <option disabled value="">请选择钢种</option>
        <option v-for="item in selectedGradeOptions" :value="item" :key="item">{{ item }}</option>
      </select>
      <button @click="clearFilt">重置选择</button>
    </div>
    <div class="insert-wrapper">
    <div class="insert">
      <input type="file" ref="fileInput" multiple @change="handleFileSelect" style="display:none">
      <button @click="selectFile">选择文件</button>
      <button @click="uploadFile">上传到数据库</button>    
      <button @click="clearSelection">清空</button>
      <div class="upload">
        <p v-if="selectedFiles.length === 0">未选择文件</p>
        <p v-else>已选中文件如下，点击文件名可取消选择：</p>
        <ul>
          <li v-for="file in selectedFiles" :key="file.name" @click="cancelSelection(file)" class="file-name">{{ file.name }}</li>
        </ul>
      </div>
      <el-dialog v-model="isModalOpen">
          <p>将为您上传以下文件：{{ beingUpload.join(', ') }}</p>
          <p>以下文件表头与数据库不一致，请重新上传：{{ mismatchUpload.join(', ') }}</p>
          <p>以下文件中包含已存在的产线，请重新上传：{{ existUpload.join(', ') }}</p>
          <button @click="closeModal">确定</button>
      </el-dialog>
    </div>
    </div>
    <div class="process">
      <button @click="sendDeleteRows" :disabled="selectedRowsIds.length === 0">删除所选行</button>
      <button @click="sendEditRows" :disabled="selectedRowsIds.length == 0">修改所选行</button>
      <button @click="sendEditHeader">修改表头</button>
      <button @click="exportData">导出数据</button>
      <p>{{MaterialDataCount +'种材料'}}</p>
      <el-dialog v-model="exportAlert">
        <p>您确定要导出材料信息数据吗？</p>
        <button @click="sendExport">确定</button>
        <button @click="cancelExport">取消</button>
      </el-dialog>
      <el-dialog v-model="deleteAlert">
        <p>您确定要删除以下数据吗？</p>
        <div class="table">
          <table>
            <thead>
              <tr>
                <th v-for="(column, index) in tableHeader" :key="index">{{ column }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in selectedData" :key="rowIndex">
                <td v-for="(value, columnName) in row" :key="columnName">{{ value }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <button @click="sendDelete">确定</button>
        <button @click="cancelDelete">取消</button>
      </el-dialog>
      <el-dialog v-model="editAlert">
        <p>您确定要编辑以下数据吗？</p>
        <div class="table">
          <table>
            <thead>
              <tr>
                <th v-for="(column, index) in tableHeader" :key="index">{{ column }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in selectedData" :key="rowIndex">
                <td v-for="(value, columnName) in row" :key="columnName">
                  <input type="text" v-model="row[columnName]">
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <button @click="sendEdit">确定</button>
        <button @click="cancelEdit">取消</button>
      </el-dialog>
      <el-dialog v-model="headerAlert">
        <p>您确定要编辑表头吗？</p>
        <div class="table">
          <table>
            <thead>
              <tr>
                <th v-for="(column, index) in tableHeader" :key="index">{{ column }}</th>
              </tr>
            </thead>
            <tbody>
              <td v-for="(row, rowIndex) in tableHeader" :key="rowIndex">
                  <input type="text" v-model="tableHeader[rowIndex]">
              </td>
            </tbody>
          </table>
        </div>
        <button @click="sendHeader">确定</button>
        <button @click="cancelHeader">取消</button>
      </el-dialog>
    </div>
    <div class="table">
      <table>
        <thead>
          <tr>
            <th>
              <input type="checkbox" v-model="selectAll" @change="toggleSelectAll">
            </th>
            <th v-for="(column, index) in tableHeader" :key="index">{{ column }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in tableData" :key="rowIndex">
            <td>
              <input type="checkbox" :value="row[0]" v-model="selectedRowsIds" />
            </td>
            <td v-for="(column, columnIndex) in row" :key="columnIndex">
                {{ column }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import {GET_MATERIAL_DATA} from '@/config'
import {SELECTED_TYPE} from '@/config'
import {SELECTED_TYPE1} from '@/config'
import {SELECTED_TYPE2} from '@/config'
import {SELECTED_GRADE} from '@/config'
import {SELECT_MATERIALS} from '@/config'
import {DELETE_MATERIALS} from '@/config'
import {EDIT_MATERIALS} from '@/config'
import {UPLOAD_MATERIAL} from '@/config'
import {EDIT_MATERIAL_HEADER} from '@/config'
import {EXPORT_MATERIAL} from '@/config'

export default {
  data() {
    return {
      tableHeader: [],
      tableData: [],

      selectedTypeOptions: [],//下拉产线
      selectedType1Options: [],//下拉产线
      selectedType2Options: [],//下拉产线
      selectedGradeOptions: [],//下拉产线
      selectedType:'',//所选产线
      selectedType1:'',//所选工厂
      selectedType2:'',//所选工厂
      selectedGrade:'',//所选工厂


      selectAll: false,
      headerAlert: false,
      selectedRowsIds: [], // 存储选中行的标识符
      deleteAlert:false,//是否显示删除确认弹窗
      editAlert:false,//是否显示编辑确认弹窗
      selectedFiles: [],
      isModalOpen: false,
      exportAlert: false,
    }
  },
  mounted() {
    fetch(GET_MATERIAL_DATA)
      .then(response => response.json())
      .then(data => {
        if (data.tableHeader && data.tableData) {
          this.MaterialDataCount = data.MaterialDataCount;
          this.tableHeader = data.tableHeader;
          this.tableData = data.tableData;          
          this.selectedTypeOptions = data.selectedTypeOptions;
          this.selectedType1Options = data.selectedType1Options;
          this.selectedType2Options = data.selectedType2Options;
          this.selectedGradeOptions = data.selectedGradeOptions;
        }
      });
  },
  computed: {
    selectedRows() {
      return this.tableData.filter(row => this.selectedRowsIds.includes(row[0]));
    }
  },
  methods: {
    sendselectedType() {
      fetch(SELECTED_TYPE, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            selectedType: this.selectedType,
          })
          })
          .then(response => response.json())
          .then(data => {
            console.log('所选产线传回成功', data);
            this.tableData = data;
          })
          .catch(error => {
            console.error('传回失败', error);
          });
    },
    sendselectedType1() {
        fetch(SELECTED_TYPE1, {
              method: 'POST',
              headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              selectedType1: this.selectedType1,
            })
            })
            .then(response => response.json())
            .then(data => {
              console.log('所选工厂传回成功', data);
              this.tableData = data;
            })
            .catch(error => {
              console.error('传回失败', error);
            });
    },
    sendselectedType2() {
        fetch(SELECTED_TYPE2, {
              method: 'POST',
              headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              selectedType2: this.selectedType2,
            })
            })
            .then(response => response.json())
            .then(data => {
              console.log('所选工厂传回成功', data);
              this.tableData = data;
            })
            .catch(error => {
              console.error('传回失败', error);
            });
    },
    sendselectedGrade() {
        fetch(SELECTED_GRADE, {
              method: 'POST',
              headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              selectedGrade: this.selectedGrade,
            })
            })
            .then(response => response.json())
            .then(data => {
              console.log('所选工厂传回成功', data);
              this.tableData = data;
            })
            .catch(error => {
              console.error('传回失败', error);
            });
    },
    clearFilt() {

      this.selectedType = '';
      this.selectedType1 = '';
      this.selectedType2 = '';
      this.selectedGrade = '';

      fetch(GET_MATERIAL_DATA)
      .then(response => response.json())
      .then(data => {
        if (data.tableHeader && data.tableData) {
          this.tableData = data.tableData;          
        }
      });
    },


    toggleSelectAll() {
      if (this.selectAll) {
        this.selectedRowsIds = this.tableData.map(row => row[0]);
      } else {
        this.selectedRowsIds = [];
      }
    },
    handleFileSelect(event) {
      const files = event.target.files;
      Array.from(files).forEach(file => {
        const existedFile = this.selectedFiles.find(f => f.name === file.name);
        if (existedFile) {
          this.cancelSelection(existedFile);
        } else {
          this.selectedFiles.push(file);
        }
      });
      event.target.value = '';
    },
    selectFile() {
      this.$refs.fileInput.click();
    },
    uploadFile() {
      if (this.selectedFiles.length === 0) {
        alert('请先选择文件');
        return;
      }
      const formData = new FormData();
      this.selectedFiles.forEach(file => {
        formData.append('file', file);
      });
      fetch(UPLOAD_MATERIAL, {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        // 处理上传成功的响应
        console.log('上传成功', data);
        this.beingUpload = data.beingUpload;
        this.mismatchUpload = data.mismatchUpload;
        this.existUpload = data.existUpload;
        this.tableData = data.tableData;
        this.isModalOpen = true;
      })
      .catch(error => {
        // 处理上传失败的情况
        console.error('上传失败', error);
      });
      this.selectedFiles = [];
    },   
    closeModal() {
      this.isModalOpen = false;
    },
    cancelSelection(file) {
      const index = this.selectedFiles.indexOf(file);
      if (index > -1) {
        this.selectedFiles.splice(index, 1);
      }

      // 清空 input 元素的选择列表
      this.$refs.fileInput.value = '';
    },
    clearSelection() {
      this.selectedFiles = [];
      // 清空文件输入框
      const input = this.$refs.fileInput;
      input.value = '';
    },
    sendDeleteRows() {
      fetch(SELECT_MATERIALS, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedRowsIds: this.selectedRowsIds
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('选中删除数据成功', data);
      this.selectedData = data.selectedData;
      this.deleteAlert = true;
    })
    .catch(error => {
      console.error('传回失败', error);
    });
    },
    sendDelete(){
      fetch(DELETE_MATERIALS, {
        method: 'POST',
        body: JSON.stringify({ selectedRowsIds: this.selectedRowsIds }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log('删除数据成功', data);
          this.deleteAlert = false;
          this.selectedRowsIds = [];
          this.tableData = data.tableData;
          this.MaterialDataCount = data.MaterialDataCount
        });
    },
    cancelDelete() {
      this.deleteAlert = false;
    },
    sendEditRows() {
      fetch(SELECT_MATERIALS, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedRowsIds: this.selectedRowsIds
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('选中编辑数据成功', data);
      this.selectedData = data.selectedData;
      this.editAlert = true;
    })
    .catch(error => {
      console.error('传回失败', error);
    });
    },
    sendEdit(){
      fetch(EDIT_MATERIALS, {
        method: 'POST',
        body: JSON.stringify({ selectedRowsIds: this.selectedRowsIds,
        updateData:this.selectedData
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log('编辑数据成功', data);
          this.editAlert = false;
          this.selectedRowsIds = [];
          this.tableData = data.tableData;
        });
    },
    cancelEdit() {
      this.editAlert = false;
    },
    sendEditHeader() {
      this.headerAlert = true;
    },
    sendHeader(){
      fetch(EDIT_MATERIAL_HEADER, {
        method: 'POST',
        body: JSON.stringify({ updateHeader:this.tableHeader }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log('编辑数据成功', data);
          this.headerAlert = false;
          this.tableHeader = data.tableHeader;
        });
    },
    cancelHeader() {
      this.headerAlert = false;
    },
    exportData() {
      this.exportAlert = true;
    },
    sendExport() {
      // 发送导出请求
      window.location.href = EXPORT_MATERIAL; // 发送到后端的路由
      this.exportAlert = false; // 关闭确认对话框
    },
    cancelExport() {
      this.exportAlert = false;
    },
  }
};
</script>

<style scoped>
.el-header {
  background-color: #545c64;
  color: #f6f6f6;
  text-align: center;
  line-height: 60px;
  width: 100%;
  font-size: 24px;
}
.vertical-options {
  flex-direction: column; /* 设置弹出层为纵向排列 */
}
.insert-wrapper {
  color: #000000;
  position: relative;
  width:100%;
  border: 1px solid #ccc;
  margin-top:20px;
}
.file-name {
  color: #000000; /* 设置文件名颜色为黑色 */
  font-size: 14px;
}
.table {
    max-height: 500px; /* 设置最大高度 */
    overflow-y: auto; /* 添加垂直滚动条 */
    border: 1px solid #ccc; /* 添加边框 */
}
table {
  border-collapse: collapse;
}
th, td {
  border: 1px solid #5b5b5b;
  padding: 8px;
  text-align: left;
  vertical-align: top;
  white-space: nowrap; /* 阻止表头文本换行 */
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
</style>