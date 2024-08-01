<template>
  <div class="image-container">
      <h1>板带轧制基础模型库/生产数据库</h1>
    </div>
    <div class="intro-container">
      <h1 id="intro">— 模型/数据整合应用 —</h1>
      <p id="intro-under">基于塑性加工和物理冶金原理，研究多尺度耦合分析的关键工艺质量参数高精度解析与数值计算方法，
        构建多因素耦合作用下的载荷特性求解与材料组织演变综合模型，建立轧制过程力能参数、负荷分配、工艺温度、三维变形、微观组织与力学性能等基础机理模型库，
        构建涵盖典型钢铁材料、各类差异化生产线工艺的数据库。</p>
    </div>
    <router-link id="link1" to="/" class="custom-link1">
    <img src="./home.jpg" alt="Image" class="link-img1">
    <span class="link-text">回到首页</span>
  </router-link>
  <router-link id="link2" to="/line" class="custom-link2">
    <img src="./home.jpg" alt="Image" class="link-img2">
    <span class="link-text">产线基础信息</span>
  </router-link>
  <router-link id="link3" to="/material" class="custom-link3">
    <img src="./home.jpg" alt="Image" class="link-img3">
    <span class="link-text">材料信息</span>
  </router-link>
  
    <div class="safeguard-container">
    </div>
    </template>
  
  
    <style scoped>
    .image-container {
     display: flex;
    background: url('./image.png');
    background-size: cover; 
    position: absolute;
    top: 80px;
    left: 0;
    width: 100%;
    height:70%;
  }
  .image-container h1{
    position: relative;
      top: 50%;
      left:30%;
      font-size: 40px;
  }
  .intro-container{
    text-align:center;
    position: absolute;
    top: 80%;
    left: 0;
    width: 100%;
    height:200px;
  }
  .custom-link1 {
    display: inline-block;
    text-decoration: none;
    color: #000;
    border: dashed black 1px;
    position:absolute;
    top:105%;
    left:2%;
    width:30%;
  }
  .link-img1 {
    width: 100%; /* 调整图片的宽度 */
    height: auto; /* 保持图片的纵横比 */
  }
  .custom-link2{
    display: inline-block;
    text-decoration: none;
    color: #000;
    border: dashed black 1px;
    position:absolute;
    top:105%;
    left:35%;
    width:30%;
  }
  .link-img2 {
    width: 100%; /* 调整图片的宽度 */
    height: auto; /* 保持图片的纵横比 */
  }
  

  .custom-link3 {
    display: inline-block;
    text-decoration: none;
    color: #000;
    border: dashed black 1px;
    position:absolute;
    top:105%;
    left:68%;
    width:30%;
  }
  .link-img3 {
    width: 100%; /* 调整图片的宽度 */
    height: auto; /* 保持图片的纵横比 */
  }

  .safeguard-container {
    display: flex;
    background-color:#000000;
    background-size: cover; 
    position: absolute;
    top: 150%;
    left: 0;
    width: 100%;
    height:5%;
  }
    </style>