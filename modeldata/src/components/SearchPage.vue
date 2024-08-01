<!-- ContentPage.vue -->
<template>
    <div>
      <el-header>
        {{ $route.params.searchKeyword + ' ' + currentModelnum  + '/' + modelNum}}    
        <div class="search-container">      
        <link rel="stylesheet" href="https://cdn.staticfile.org/font-awesome/4.7.0/css/font-awesome.css">
        <input class="sousuo" type="text" v-model="newKeyword" placeholder="搜索模型">
          <i class="search-icon fa fa-search" aria-hidden="true"@click="search"></i>
      </div>
      </el-header>

      <div class="label-container"
    @wheel="handleWheel"
    @mousedown="startDrag"
    @mousemove="onDrag"
    @mouseup="endDrag"
    tabindex="0">
    <ul>
          <li v-for="item in searchData" :key="item.chineseName">
              <router-link :to="getRoute(item)" class="link">
                  <div class="label-content">
                      <div>
                          <img v-if="item.productionLine === '热连轧'" src="./rezha.jpg" alt="Image">
                          <img v-if="item.productionLine === '中厚板'" src="./zhonghouban.jpg" alt="Image">
                          <img v-if="item.productionLine === '冷轧'" src="./lengzha.jpg" alt="Image">
                          {{ '机理模型' }}
                      </div>
                      <div>
                          {{ '模型中文名称：' + truncateString(item.chineseName, 16) }}
                      </div>
                      <div>
                          {{ '模型英文名称：'+item.englishName }}
                      </div>
                      <div>
                          {{ '开发语言：'+item.language }}
                      </div>
                      <div>
                          {{ '标签：'+item.label }}
                      </div>
                  </div>
              </router-link>
          </li>
      </ul>    
      <div class="pagination-wrapper">
      <div class="pagination">
        <button @click="prevPage" :disabled="localCurrentPageNumber === 1">上一页</button>
        <span>{{ localCurrentPageNumber }} / {{ totalPages }}</span>
        <button @click="nextPage" :disabled="localCurrentPageNumber === totalPages">下一页</button>
      </div>
      </div>
    </div>
  </div>
  </template>
  
  <script>
import {SEND_SEARCH} from '@/config'
import {SEND_SEARCHITEMS} from '@/config'
  
  export default {
  data() {
    return {
    searchData:[],
    rowsPerPage: 4,
    itemsPerRow: 4,
    itemsPerPage: 16,
    currentModelnum: null,
    modelNum: null,
    localCurrentPageNumber: null,
    totalPages: 0,
    isDragging: false,
    dragStartX: 0,
    initialFontSize: 12,
    isShiftPressed: false,
    currentPageNumber: 1,
    searchKeywords: [this.$route.params.searchKeyword]
    };
  },

  watch: {
  searchKeyword: {
    immediate: true,
    handler() {
      this.localCurrentPageNumber = this.currentPageNumber;
      this.fetchSearch();
    }
  },
  currentPageNumber: {
    immediate: true,
    handler(newPageNumber) {
      this.localCurrentPageNumber = newPageNumber;  // 将 currentPageNumber 的值传给 localCurrentPageNumber
    }
  },

},
mounted() {
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
  },

  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
  },
  methods: {
    getRoute(item) {
    // 判断当前路由是否是标签页面，如果是则返回固定路由
    if (this.$route.path.includes('/modelname/')) {
      return `/model/${item.chineseName}`;
    }
    // 如果不是标签页面，则根据当前路由参数和子菜单项生成动态路由
    return `${this.$route.path}/modelname/${item.chineseName}`;
  },
  search() {
    const newKeyword = this.newKeyword;
    this.searchKeywords.push(newKeyword);
    const keywordsString = this.searchKeywords.join(',');
    const currentRoute = this.$route;
    const newPath = currentRoute.path.replace(/\/search\/[^/]+/, '/search/' + keywordsString);
    this.$router.push({ path: newPath }).then(() => {
    this.fetchSearch();
    this.newKeyword = '';
  });
  },
    fetchSearch(){
      const searchKeywords = this.$route.params.searchKeyword;
      const modelParam = this.$route.params.model;
      const model = modelParam.includes('-') ? modelParam.split('-')[0] : modelParam;

      let requestBody = {
        searchKeywords
      };
      // 检查是否存在 model 参数
      if (model) {
        requestBody.model = model;
      }
      fetch(SEND_SEARCH, {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          requestBody
        })
        })
          .then(response => response.json())
          .then(data => {
            console.log('搜索传回成功', data);
            this.updateSearchItems();
          })
          .catch(error => {
            console.error('传回失败', error);
          });
    },
    async updateSearchItems() {  
      const itemsPerPage = this.calculateItemsPerPage();
      try {
    const response = await fetch(SEND_SEARCHITEMS, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        itemsPerPage: itemsPerPage,
      })
    });

    const { data, totalPages, currentModelnum, modelNum } = await response.json();

    console.log('获取到的数据:', currentModelnum);
        // 更新总页数和当前页数据
    this.totalPages = totalPages;
    this.searchData = data;
    this.currentModelnum = currentModelnum;
    this.modelNum = modelNum;
  } catch (error) {
    console.error('获取数据时出错:', error);
  }
  },
  calculateItemsPerPage() {
  return this.itemsPerRow * this.rowsPerPage;
  },
  
  // 上一页
  prevPage() {
    if (this.localCurrentPageNumber > 1) {
      this.localCurrentPageNumber--;
      this.fetchSearch();
    }
  },

  // 下一页
  nextPage() {
    if (this.localCurrentPageNumber < this.totalPages) {
      this.localCurrentPageNumber++;
      this.fetchSearch();
    }
  },
  handleWheel(event) {
      if (this.isShiftPressed) {
        event.preventDefault(); // 阻止默认的滚动行为
        const delta = Math.sign(event.deltaY);
        const scaleFactor = delta > 0 ? 0.9 : 1.1;
        this.adjustLabelSize(scaleFactor);
      }
  },

  handleKeyDown(event) {
    if (event.key === 'Shift') {
      this.isShiftPressed = true;
    }
  },

  handleKeyUp(event) {
    if (event.key === 'Shift') {
      this.isShiftPressed = false;
    }
  },
  adjustLabelSize: function(scaleFactor) {
    const labelDivs = document.querySelectorAll('.label-content');
    labelDivs.forEach((labelDiv) => {
      const newSize = labelDiv.clientWidth * scaleFactor; // 根据元素宽度调整整个标签大小
      labelDiv.style.width = `${newSize}px`;
      labelDiv.style.height = `${newSize}px`;
    });
    this.calculateItemsPerRow();
    this.itemsPerPage = this.calculateItemsPerPage();
  },

  calculateItemsPerRow: function () {
    const labelContainer = document.querySelector('.label-container');
    const labelDiv = document.querySelector('.label-content');

    if (labelContainer && labelDiv) {
      const containerWidth = labelContainer.clientWidth;
      const labelWidth = labelDiv.clientWidth;

      // 计算每行包含的标签数
      this.itemsPerRow = Math.floor(containerWidth / labelWidth);
    }
  },
  truncateString(str, maxLength) {
    return str.length > maxLength ? str.slice(0, maxLength) + '...' : str;
  },
  }
  }
  </script>
  <style>
  .el-header {
    background-color: #545c64;
    color: #f6f6f6;
    text-align: center;
    line-height: 60px;
    width: 100%;
    font-size: 24px;
  }
  h2 {
    text-align: center;
  }
  
  .search-container {
  position: absolute;
  display: inline-block;
  right: 5%;
}

.sousuo[type="text"] {
  padding: 10px 40px 10px 10px;
  border-radius: 20px;
  font-size: 16px;
  width: 300px;
}

.search-icon {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  color: #666;
  cursor: pointer;
}
.sousuo[type="text"]:focus {
  outline: none;
  border-color: #999;
}

.sousuo[type="text"]:focus + .search-icon {
  color: #333;
}
  .label-container{
    position: relative;
    width:100%;
    border: 1px solid #ccc;
  }
  ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-wrap: wrap;
  }
  .label-content {
      display: inline-block;
      text-decoration: none;
      font-size: 12px;
      color: #000;
      border: dashed black 1px;
      width: 300px;
      height: 265px;
      margin: 10px;
      transform-origin: top left;
  }
    .label-content img {
      max-width: 100%;
      max-height: 100%;
    }
  .pagination-wrapper {
    display: flex;
    justify-content: center;
  }
  .pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 20%; 
    width: 100%; 
  }
  
  button {
    border-radius: 4px;
    cursor: pointer;
    width:80px;
    height:30px;
  }
  </style>