<template>
  <div class="app-container">
    <el-card class="box-card">
      <h4>{{ $t('goods_edit.section.goods') }}</h4>
    </el-card>

    <!-- 查询结果 -->
    <el-table v-loading="listLoading" :data="list" :element-loading-text="$t('app.message.list_loading')" border fit highlight-current-row @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" />
      <el-table-column align="center" :label="$t('商品ID')" prop="id" />

      <el-table-column align="center" min-width="100" :label="$t('商品名称')" prop="name" />

      <el-table-column align="center" property="iconUrl" :label="$t('首图')">
        <template slot-scope="scope">
          <el-image :src="thumbnail(scope.row.picUrl)" :preview-src-list="toPreview(scope.row, scope.row.picUrl)" style="width: 40px; height: 40px" />
        </template>
      </el-table-column>

      <el-table-column align="center" :label="$t('详情')" prop="detail">
        <template slot-scope="scope">
          <el-dialog :visible.sync="detailDialogVisible" :title="$t('goods_list.dialog.detail')">
            <div class="goods-detail-box" v-html="goodsDetail" />
          </el-dialog>
          <el-button type="primary" size="mini" @click="showDetail(scope.row.detail)">{{ $t('查看') }}</el-button>
        </template>
      </el-table-column>

      <el-table-column align="center" :label="$t('goods_list.table.actions')" width="200" class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button type="primary" size="mini" @click="handleUpdate(scope.row)">{{ $t('编辑') }}</el-button>
          <el-button type="danger" size="mini" @click="handleDelete(scope.row)">{{ $t('删除') }}</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <el-tooltip placement="top" :content="$t('app.tooltip.back_to_top')">
      <back-to-top :visibility-height="100" />
    </el-tooltip>

  </div>
</template>

<style>
  .table-expand {
    font-size: 0;
    padding-left: 60px;
  }
  .table-expand label {
    width: 100px;
    color: #99a9bf;
  }
  .table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
  }
  .gallery {
    width: 80px;
    margin-right: 10px;
  }
  .goods-detail-box img {
    width: 100%;
  }
</style>

<script>
import { listGoods, deleteGoods, listGoodStock } from '@/api/goods'
import BackToTop from '@/components/BackToTop'
import Pagination from '@/components/Pagination' // Secondary package based on el-pagination
import { thumbnail, toPreview } from '@/utils/index'

export default {
  name: 'GoodsList',
  components: { BackToTop, Pagination },
  data() {
    return {
      batchDeleteArr: [],
      thumbnail,
      toPreview,
      list: [],
      total: 0,
      goodsInfo: {},
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20,
        goodsSn: undefined,
        name: undefined,
        sort: 'add_time',
        order: 'desc'
      },
      goodsDetail: '',
      detailDialogVisible: false,
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      listGoodStock({ 'goodsId': this.$route.query.id }).then(response => {
        console.log(response.data)
        this.list = response.data.data.stock
        this.total = response.data.data.total
        this.goodsInfo = response.data.data.goods
        this.listLoading = false
      }).catch(() => {
        this.list = []
        this.total = 0
        this.listLoading = false
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    handleCreate() {
      this.$router.push({ path: '/resource/create' })
    },
    handleUpdate(row) {
      this.$router.push({ path: '/resource/edit', query: { id: row.id }})
    },
    showDetail(detail) {
      this.goodsDetail = detail
      this.detailDialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('确定删除?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        center: true
      }).then(() => {
        deleteGoods(row).then(response => {
          this.$notify.success({
            title: '成功',
            message: '删除成功'
          })
          this.getList()
        }).catch(response => {
          this.$notify.error({
            title: '失败',
            message: response.data.errmsg
          })
        })
      }).catch(() => {})
    },
    handleSelectionChange(val) {
      console.log(val)
      this.batchDeleteArr = val
    },
    handleDeleteRows() {
      this.batchDeleteArr.forEach(row => this.handleDeleteEachRow(row))
      this.getList()
    },
    handleDeleteEachRow(row) {
      deleteGoods(row).then(response => {
        this.$notify.success({
          title: '成功',
          message: '删除成功'
        })
      }).catch(response => {
        this.$notify.error({
          title: '失败',
          message: response.data.errmsg
        })
      })
    },
    handleDownload() {
      this.downloadLoading = true
      import('@/vendor/Export2Excel').then(excel => {
        const tHeader = ['商品ID', '商品编号', '名称', '专柜价格', '当前价格', '是否新品', '是否热品', '是否在售', '首页主图', '宣传图片列表', '商品介绍', '详细介绍', '商品图片', '商品单位', '关键字', '类目ID', '品牌商ID']
        const filterVal = ['id', 'goodsSn', 'name', 'counterPrice', 'retailPrice', 'isNew', 'isHot', 'isOnSale', 'listPicUrl', 'gallery', 'brief', 'detail', 'picUrl', 'goodsUnit', 'keywords', 'categoryId', 'brandId']
        excel.export_json_to_excel2(tHeader, this.list, filterVal, '商品信息')
        this.downloadLoading = false
      })
    }
  }
}
</script>
