<template>
  <div>
    <el-header>产线生产信息数据库</el-header>
    <div class="filters">
      <select v-model="selectedPline" @change="sendselectedPline">
        <option disabled value="">请选择产线</option>
        <option v-for="item in selectedPlineOptions" :value="item" :key="item">{{ item }}</option>
      </select>
      <select v-model="selectedGradename" @change="sendselectedGradename">
        <option disabled value="">请选择钢种</option>
        <option v-for="item in selectedGradenameOptions" :value="item" :key="item">{{ item }}</option>
      </select>
      <select v-model="selectedWidth" @change="sendselectedWidth">
        <option disabled value="">请选择宽度</option>
        <option v-for="(item, index) in selectedWidthOptions" :key="index" :value="item[0]">{{ item[1] }} ~ {{ item[2] }}</option>
        <option :value="17">{{ maxWidthOption }} ~ ∞</option>
      </select>
      <select v-model="selectedThick" @change="sendselectedThick">
        <option disabled value="">请选择厚度</option>
        <option v-for="(item, index) in selectedThickOptions" :key="index" :value="item[0]">{{ item[1] }} ~ {{ item[2] }}</option>
        <option :value="14">{{ maxThickOption }} ~ ∞</option>
      </select>
      <button @click="clearFilt">重置选择</button>
      <p>{{SelectProductLineCount + '条/' + TotalProductLineData + '条'}}</p> 
    </div>
    <div>
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
      <button @click="exportData">导出数据</button>
      <el-dialog v-model="exportAlert">
        <p>请选择筛选条件</p>
        <select v-model="exportGradename">
          <option disabled value="">请选择钢种</option>
          <option v-for="item in selectedGradenameOptions" :value="item" :key="item">{{ item }}</option>
        </select>
        <select v-model="exportWidth">
          <option disabled value="">请选择宽度</option>
          <option v-for="(item, index) in selectedWidthOptions" :key="index" :value="item[0]">{{ item[1] }} ~ {{ item[2] }}</option>
        </select>

        <select v-model="exportThick">
          <option disabled value="">请选择厚度</option>
          <option v-for="(item, index) in selectedThickOptions" :key="index" :value="item[0]">{{ item[1] }} ~ {{ item[2] }}</option>
        </select>
        <button @click="clearExport">重置筛选</button>
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
    <div>
      <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
    </div>
  </div>
</template>

<script>
import {GET_PRODUCT_DATA} from '@/config'
import {SEND_SELECTED_PLINE} from '@/config'
import {SEND_SELECTED_GRADENAME} from '@/config'
import {SEND_SELECTED_WIDTH} from '@/config'
import {SEND_SELECTED_THICK} from '@/config'
import {SELECT_PRODUCTS} from '@/config'
import {DELETE_PRODUCTS} from '@/config'
import {UPLOAD_PRODUCT} from '@/config'
import {EXPORT_PRODUCT} from '@/config'
export default {
  data() {
    return {
      tableHeader: [],
      tableData: [],

      selectedPlineOptions: [],//下拉产线
      selectedGradenameOptions: [],//下拉产线
      selectedWidthOptions: [],//下拉产线
      selectedThickOptions: [],//下拉产线
      maxWidthOption: '',
      maxThickOption: '',
      selectedPline:'',//所选产线
      selectedGradename:'',//所选工厂
      selectedWidth:'',
      selectedThick:'',
      slabWidth:'',
      slabThick:'',
      currentPage: 1,
      totalPages: 1,
      pageSize: 10, // 每页显示的行数

      selectAll: false,
      selectedRowsIds: [], // 存储选中行的标识符
      deleteAlert:false,//是否显示删除确认弹窗
      selectedFiles: [],
      isModalOpen: false,
      exportAlert: false,
      exportGradename:'',//所选工厂
      exportWidth:'',
      exportThick:'',
    }
  },
  mounted() {
    fetch(GET_PRODUCT_DATA)
      .then(response => response.json())
      .then(data => {
          this.ProductLineCount = data.ProductLineCount;
          this.TotalProductLineData = data.TotalProductLineData;
          this.ProductLineData = data.ProductLineData;
          this.selectedPlineOptions = data.selectedPlineOptions;
          console.log('所选产线传回成功', data);
      });
  },
  computed: {
    selectedRows() {
      return this.tableData.filter(row => this.selectedRowsIds.includes(row[0]));
    }
  },
  methods: {
    sendselectedPline() {
      fetch(SEND_SELECTED_PLINE, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            selectedPline: this.selectedPline,
            page: this.currentPage,
            pageSize: this.pageSize
          })
          })
          .then(response => response.json())
          .then(data => {
            console.log('所选产线传回成功', data);
              this.SelectProductLineCount = data.SelectProductLineCount;
              this.tableHeader = data.tableHeader;
              this.tableData = data.tableData;          
              this.selectedGradenameOptions = data.selectedGradenameOptions;
              this.selectedWidthOptions = data.selectedWidthOptions;
              this.selectedThickOptions = data.selectedThickOptions;
              this.maxWidthOption = data.maxWidthOption;
              this.maxThickOption = data.maxThickOption;
              this.totalPages = Math.ceil(data.totalRows / this.pageSize);
          })
          .catch(error => {
            console.error('传回失败', error);
          });
    },
prevPage() {
  if (this.currentPage > 1) {
    this.currentPage--;
    if (this.selectedGradename) {
      this.sendselectedGradename(); // 如果有筛选条件，调用发送筛选数据的函数
    } else if (this.selectedDate) {
      this.sendselectedDate(); // 如果有筛选条件，调用发送筛选数据的函数
    } else if (this.selectedWidth) {
      this.sendselectedWidth(); // 如果有筛选条件，调用发送筛选数据的函数
    } else if (this.selectedThick) {
      this.sendselectedThick(); // 如果有筛选条件，调用发送筛选数据的函数
    } else {
      this.sendselectedPline(); // 否则调用发送原始数据的函数
    }
  }
},
nextPage() {
  if (this.currentPage < this.totalPages) {
    this.currentPage++;
    if (this.selectedGradename) {
      this.sendselectedGradename(); // 如果有筛选条件，调用发送筛选数据的函数
    } else if (this.selectedDate) {
      this.sendselectedDate(); // 如果有筛选条件，调用发送筛选数据的函数
    } else if (this.selectedWidth) {
      this.sendselectedWidth(); // 如果有筛选条件，调用发送筛选数据的函数
    } else if (this.selectedThick) {
      this.sendselectedThick(); // 如果有筛选条件，调用发送筛选数据的函数
    } else {
      this.sendselectedPline(); // 否则调用发送原始数据的函数
    }
  }
},
    sendselectedGradename() {
      fetch(SEND_SELECTED_GRADENAME, {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            selectedGradename: this.selectedGradename,
            page: this.currentPage,
            pageSize: this.pageSize
          })
          })
          .then(response => response.json())
          .then(data => {
            console.log('所选工厂传回成功', data);
            this.tableData = data.Data;
            this.totalPages = data.totalPages
          })
          .catch(error => {
            console.error('传回失败', error);
          });
    },

    sendselectedWidth(){
      fetch(SEND_SELECTED_WIDTH, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedWidth: this.selectedWidth,
          page: this.currentPage,
          pageSize: this.pageSize
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log('所选工厂传回成功', data);
          this.tableData = data.Data;
          this.totalPages = data.totalPages
        })
        .catch(error => {
          console.error('传回失败', error);
        });
    },
    sendselectedThick(){
      fetch(SEND_SELECTED_THICK, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          selectedThick: this.selectedThick,
          page: this.currentPage,
          pageSize: this.pageSize
        })
        })
        .then(response => response.json())
        .then(data => {
          console.log('所选工厂传回成功', data);
          this.tableData = data.Data;
          this.totalPages = data.totalPages
        })
        .catch(error => {
          console.error('传回失败', error);
        });
    },
    clearFilt() {
      this.selectedGradename = '';
      this.selectedWidth = '';
      this.selectedThick = '';
      this.sendselectedPline();
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
      fetch(UPLOAD_PRODUCT, {
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
      fetch(SELECT_PRODUCTS, {
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
      fetch(DELETE_PRODUCTS, {
        method: 'POST',
        body: JSON.stringify({ selectedRowsIds: this.selectedRowsIds }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log('删除数据成功', data);
          this.selectedRowsIds = [];
          this.tableData = data.tableData;
          this.deleteAlert = false;
        });
    },
    cancelDelete() {
      this.deleteAlert = false;
    },
    exportData() {
      this.exportAlert = true;
    },
    clearExport() {
      this.exportGradename = '';
      this.exportWidth = '';
      this.exportThick = '';
      // this.sendselectedPline();
    },
    sendExport() {
      const filterUrl = EXPORT_PRODUCT + `?exportGradename=${encodeURIComponent(this.exportGradename)}&exportWidth=${encodeURIComponent(this.exportWidth)}&exportThick=${encodeURIComponent(this.exportThick)}`;
      // 页面重定向到导出数据的 URL
      window.location.href = filterUrl;
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
  margin-top:20px;
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