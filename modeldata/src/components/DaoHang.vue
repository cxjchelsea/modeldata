<template>
  <div>
    <div class="guide-container">  
      <router-link to="/" class="logo">
        <img src="./logo.png" alt="Image">
      </router-link>
      <ul>
        <li @mouseover="showSubMenu('database')" @mouseleave="hideSubMenu('database')">数据库
          <ul v-if="isDatabaseSubMenuVisible" class="submenu">
            <li><router-link to="/line" class="submenu-link">产线基础信息</router-link></li>
            <li><router-link to="/material" class="submenu-link">材料信息</router-link></li>
            <li><router-link to="/product" class="submenu-link">生产信息</router-link></li>
          </ul>
        </li>
        <li class='menu-item' @mouseover="showSubMenu('model')" @mouseleave="hideSubMenu('model')">
          <router-link @click="changePage('模型')" to="/model" class="submenu-link">模型库</router-link>
          <ul v-if="isModelSubMenuVisible" class="submenu">
            <li v-for="item in modelList" :key="item.name" @mouseover="showThirdMenu(item)" @mouseleave="hideThirdMenu(item)">
              <router-link @click="changePage(item.name)" :to="'/model/' + item.name" class="submenu-link">{{ item.name }}</router-link>
              <ul v-if="item.isSubMenuVisible" class="subsubmenu">
                <li v-for="subItem in item.subMenu" :key="subItem">
                  <router-link @click="changePage(subItem)" :to="'/model/' + subItem" class="submenu-link">{{ subItem }}</router-link>
                </li>
              </ul>
            </li>
          </ul>
        </li>
        <li><router-link to="/Weihu" class="menu-item">维护</router-link></li>
      </ul>      
      <button @click="logOut">退出登录</button>
    </div>
    <router-view :current-page="currentPage" :currentPageNumber="currentPageNumber" :isAdmin="isAdmin"></router-view>
  </div>
</template>

<script>
export default {
  name: 'DaoHang',
  props: {
    isAdmin: Boolean, // 声明 isAdmin 作为 prop
  },
  data() {
    return {
      isDatabaseSubMenuVisible: false,
      isModelSubMenuVisible: false,
      modelList:[
        { name: "力能参数", subMenu: ["力能参数-热连轧", "力能参数-中厚板", "力能参数-冷轧"], isSubMenuVisible: false },
        { name: "负荷分配", subMenu: ["负荷分配-热连轧", "负荷分配-中厚板", "负荷分配-冷轧"], isSubMenuVisible: false },
        { name: "工艺温度", subMenu: ["工艺温度-热连轧", "工艺温度-中厚板", "工艺温度-冷轧"], isSubMenuVisible: false },
        { name: "三维变形", subMenu: ["三维变形-热连轧", "三维变形-中厚板", "三维变形-冷轧"], isSubMenuVisible: false },
        { name: "微观组织", subMenu: ["微观组织-热连轧", "微观组织-中厚板", "微观组织-冷轧"], isSubMenuVisible: false },
        { name: "力学性能", subMenu: ["力学性能-热连轧", "力学性能-中厚板", "力学性能-冷轧"], isSubMenuVisible: false },
      ]
    };
  },
  methods: {   
  logOut() {
    localStorage.removeItem('loggedIn');
    this.$emit('logout');
    this.$router.push('/');
  },
  changePage(page) {
    this.$emit("changePage", page);
    this.currentPage = page;
    this.currentPageNumber = 1;
  }, 
    showSubMenu(menuType) {
      if (menuType === 'database') {
        this.isDatabaseSubMenuVisible = true;
      } else if (menuType === 'model') {
        this.isModelSubMenuVisible = true;
      }
    },
    hideSubMenu(menuType) {
      if (menuType === 'database') {
        this.isDatabaseSubMenuVisible = false;
      }if (menuType === 'model') {
        this.isModelSubMenuVisible = false;
      }
    },
    showThirdMenu(item) {
      item.isSubMenuVisible = true;
    },
    hideThirdMenu(item) {
      item.isSubMenuVisible = false;
    }
  },
}
</script>
<style>
.guide-container {
background-color: #000000;
padding: 10px;
display: flex; /* 使用 flex 布局 */
align-items: center; /* 垂直居中 */
height:50px;
}
.logo {
cursor: pointer;
margin-right: 120px; /* 设置 logo 右边距离，以避免与主菜单项过于靠近 */
}
.menu-item {
margin-left: 80px; /* 设置主菜单项之间的右边距 */
text-decoration: none;
color: white;
}
ul {
list-style-type: none;
padding: 0;
margin: 0;
display: flex; /* 使用 flex 布局 */
font-size: 24px;
}
li {
padding: 20px;
color: white;
cursor: pointer;
position: relative;
}
li:hover ul {
display: block;
}
.submenu {
display: none;
position: absolute;
top: 100%;
left: 0;
width: 150px;
background-color: #555;
font-size: 18px;
z-index: 10; /* 设置一个较高的z-index值 */
}
.submenu li {
display: block;
}
.submenu li:hover {
background-color: #777; /* 悬停时的背景颜色 */
}
.subsubmenu {
  display: none;
  position: absolute;
  top: 0;
  left: 100%; /* 放置在父菜单项的右侧 */
  width: 180px;
  background-color: #555;
  font-size: 18px;
  z-index: 10;
}
.submenu li:hover .subsubmenu {
  display: block;
}
.submenu-link {
text-decoration: none; /* 没有下划线 */
color: white; /* 白色字体颜色 */
}
</style>
