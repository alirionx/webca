<template>
  <div class="headBlock">
    <div css="hl">Certificate Authority Management - WebUI</div>
    <div class="menuBar">
      <div><router-link to="/">Authorities</router-link></div>
      <div><router-link to="/logout">logout</router-link></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HeadBlock',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.headBlock{
  position: absolute;
  left:0px;
  top:0px;
  width: 100%;
  height: 110px;
  background-color: #008d58;
  color:#fff;
  text-align: center;
}
.headBlock div[css=hl]{
  padding:20px;
  text-align: center;
  font-size: 16px;

}
.menuBar{
  position: absolute;
  right:20px;
  bottom: 4px;
}
.menuBar div{
  display: inline-block;
  font-size: 14px;
  width: 80px;
  padding: 2px;
  border-left: 2px solid #fff;
  *border-radius: 4px;
}
.menuBar div:hover{
  *text-decoration: underline;
  background-color: rgba(255, 255, 255, 0.2);
}
.menuBar div:last-child{
  border-right: 2px solid #fff;
}
.menuBar div *{
  color:#fff;
  text-decoration: none;
}
</style>
