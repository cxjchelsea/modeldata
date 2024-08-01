<template>
  <div>
    <el-header>产线基础信息数据库</el-header>
    <div class="filters">
      <select v-model="selectedLine" @change="sendselectedLine">
        <option disabled value="">请选择产线</option>
        <option v-for="item in selectedLineOptions" :value="item" :key="item">{{ item }}</option>
      </select>
      <select v-model="selectedDesign" @change="sendselectedDesign">
        <option disabled value="">请选择工厂</option>
        <option v-for="item in selectedDesignOptions" :value="item" :key="item">{{ item }}</option>
      </select>
      <el-date-picker v-model="selectedTime" type="year" placeholder="投产时间" @change="handleDateChange"></el-date-picker>
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
      <p>{{LineDataCount + '条产线基础信息数据'}}</p>
      <el-dialog v-model="exportAlert">
        <p>您确定要导出产线基础信息数据吗？</p>
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
import {GET_LINE_DATA} from '@/config'
import {SEND_SELECTED_LINE} from '@/config'
import {SEND_SELECTED_DESIGN} from '@/config'
import {SEND_SELECTED_YEAR} from '@/config'
import {SELECT_LINES} from '@/config'
import {DELETE_LINES} from '@/config'
import {EDIT_LINES} from '@/config'
import {UPLOAD_LINE} from '@/config'
import {EDIT_LINE_HEADER} from '@/config'
import {EXPORT_LINE} from '@/config'
export default {
  data() {
    return {
      tableHeader: [],
      tableData: [],

      selectedLineOptions: [],//下拉产线
      selectedDesignOptions: [],//下拉工厂
      selectedLine:'',//所选产线
      selectedDesign:'',//所选工厂
      selectedTime:null,//所选时间
      selectedYear:null,//所选时间中的年份


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
    fetch(GET_LINE_DATA)
      .then(response => response.json())
      .then(data => {
        if (data.tableHeader && data.tableData) {
          this.LineDataCount = data.LineDataCount;
          this.tableHeader = data.tableHeader;
          this.tableData = data.tableData;          
          this.selectedLineOptions = data.selectedLineOptions;
          this.selectedDesignOptions = data.selectedDesignOptions;
        }
      });
  },
  computed: {
    selectedRows() {
      return this.tableData.filter(row => this.selectedRowsIds.includes(row[0]));
    }
  },
  methods: {
    sendselectedLine() {
      fetch(SEND_SELECTED_LINE, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            selectedLine: this.selectedLine,
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
    sendselectedDesign() {
        fetch(SEND_SELECTED_DESIGN, {
              method: 'POST',
              headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              selectedDesign: this.selectedDesign,
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
    handleDateChange() {
      if (this.selectedTime) {
        const date = new Date(this.selectedTime);
        this.selectedYear = date.getFullYear();
      } else {
        this.selectedYear = null;
      }
      fetch(SEND_SELECTED_YEAR, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedYear: this.selectedYear,
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log('所选时间传回成功', data);
          this.tableData = data;
        })
        .catch(error => {
          console.error('传回失败', error);
        });
      },
    clearFilt() {
      this.selectedLine = '';
      this.selectedDesign = '';
      this.selectedTime = null;
      fetch(GET_LINE_DATA)
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
      fetch(UPLOAD_LINE, {
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
          this.LineDataCount = data.LineDataCount;
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
      fetch(SELECT_LINES, {
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
      fetch(DELETE_LINES, {
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
          this.LineDataCount = data.LineDataCount
        });
    },
    cancelDelete() {
      this.deleteAlert = false;
    },
    sendEditRows() {
      fetch(SELECT_LINES, {
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
      fetch(EDIT_LINES, {
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
      fetch(EDIT_LINE_HEADER, {
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
      window.location.href = EXPORT_LINE; // 发送到后端的路由
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
  flex-direction: column; 
}
.insert-wrapper {
  color: #000000;
  position: relative;
  width:100%;
  border: 1px solid #ccc;
  margin-top:20px;
}
.file-name {
  color: #000000; 
  font-size: 14px;
}
.table {
    max-height: 500px; 
    overflow-y: auto; 
    border: 1px solid #ccc; 
}
table {
  border-collapse: collapse;
}
th, td {
  border: 1px solid #5b5b5b;
  padding: 8px;
  text-align: left;
  vertical-align: top;
  white-space: nowrap; 
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
