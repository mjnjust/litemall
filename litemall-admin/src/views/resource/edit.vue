<template>
  <div class="app-container">

    <el-card class="box-card">
      <h3>{{ $t('goods_edit.section.goods') }}</h3>
      <el-form ref="goods" :rules="rules" :model="goods" label-width="150px">
        <el-form-item :label="$t('goods_edit.form.id')" prop="id">
          <el-input v-model="goods.id" disabled />
        </el-form-item>
        <el-form-item :label="$t('goods_edit.form.name')" prop="name">
          <el-input v-model="goods.name" />
        </el-form-item>
        <el-form-item :label="$t('goods_edit.form.pic_url')">
          <el-upload
            :headers="headers"
            :action="uploadPath"
            :show-file-list="false"
            :on-success="uploadPicUrl"
            class="avatar-uploader"
            accept=".jpg,.jpeg,.png,.gif"
          >
            <img v-if="goods.picUrl" :src="goods.picUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon" />
          </el-upload>
        </el-form-item>

        <el-form-item :label="$t('goods_edit.form.gallery')">
          <el-upload
            :action="uploadPath"
            :headers="headers"
            :limit="5"
            :file-list="galleryFileList"
            :on-exceed="uploadOverrun"
            :on-success="handleGalleryUrl"
            :on-remove="handleRemove"
            multiple
            accept=".jpg,.jpeg,.png,.gif"
            list-type="picture-card"
          >
            <i class="el-icon-plus" />
          </el-upload>
        </el-form-item>

        <el-form-item :label="$t('goods_edit.form.keywords')">
          <el-tag v-for="tag in keywords" :key="tag" closable type="primary" @close="handleClose(tag)">
            {{ tag }}
          </el-tag>
          <el-input v-if="newKeywordVisible" ref="newKeywordInput" v-model="newKeyword" class="input-new-keyword" @keyup.enter.native="handleInputConfirm" @blur="handleInputConfirm" />
          <el-button v-else class="button-new-keyword" type="primary" @click="showInput">{{ $t('app.button.add') }}</el-button>
        </el-form-item>

        <el-form-item :label="$t('goods_edit.form.brief')">
          <el-input v-model="goods.brief" />
        </el-form-item>

        <el-form-item :label="$t('goods_edit.form.detail')">
          <editor v-model="goods.detail" :init="editorInit" />
        </el-form-item>
      </el-form>
    </el-card>

    <div class="op-container">
      <el-button @click="handleCancel">{{ $t('app.button.cancel') }}</el-button>
      <el-button type="primary" @click="handleEdit">{{ $t('goods_edit.button.edit') }}</el-button>
    </div>

  </div>
</template>

<style>
.el-card {
  margin-bottom: 10px;
}
.el-tag + .el-tag {
  margin-left: 10px;
}
.input-new-keyword {
  width: 90px;
  margin-left: 10px;
  vertical-align: bottom;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #20a0ff;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 120px;
  line-height: 120px;
  text-align: center;
}
.avatar {
  width: 145px;
  height: 145px;
  display: block;
}
.op-container {
  display: flex;
  justify-content: center;
}
</style>

<script>
import { detailGoods, editGoods, listCatAndBrand } from '@/api/goods'
import { createStorage, uploadPath } from '@/api/storage'
import Editor from '@tinymce/tinymce-vue'
import { MessageBox } from 'element-ui'
import { getToken } from '@/utils/auth'

export default {
  name: 'GoodsEdit',
  components: { Editor },
  data() {
    return {
      uploadPath,
      newKeywordVisible: false,
      newKeyword: '',
      keywords: [],
      galleryFileList: [],
      categoryList: [],
      brandList: [],
      categoryIds: [],
      goods: { gallery: [] },
      specVisiable: false,
      specForm: { specification: '', value: '', picUrl: '' },
      specifications: [{ specification: '规格', value: '标准', picUrl: '' }],
      productVisiable: false,
      productForm: {
        id: 0,
        specifications: [],
        price: 0.0,
        number: 0,
        url: ''
      },
      products: [
        { id: 0, specifications: ['标准'], price: 0.0, number: 0, url: '' }
      ],
      attributeVisiable: false,
      attributeAdd: true,
      attributeForm: { attribute: '', value: '' },
      attributes: [],
      rules: {
        name: [{ required: true, message: '商品名称不能为空', trigger: 'blur' }]
      },
      editorInit: {
        language: 'zh_CN',
        height: '400px',
        convert_urls: false,
        plugins: [
          'advlist anchor autolink autosave code codesample colorpicker colorpicker contextmenu directionality emoticons fullscreen hr image imagetools importcss insertdatetime link lists media nonbreaking noneditable pagebreak paste preview print save searchreplace spellchecker tabfocus table template textcolor textpattern visualblocks visualchars wordcount'
        ],
        toolbar: [
          'searchreplace bold italic underline strikethrough alignleft aligncenter alignright outdent indent  blockquote undo redo removeformat subscript superscript code codesample',
          'hr bullist numlist link image charmap preview anchor pagebreak insertdatetime media table emoticons forecolor backcolor fullscreen'
        ],
        images_upload_handler: function(blobInfo, success, failure) {
          const formData = new FormData()
          formData.append('file', blobInfo.blob())
          createStorage(formData)
            .then(res => {
              success(res.data.data.url)
            })
            .catch(() => {
              failure('上传失败，请重新上传')
            })
        }
      }
    }
  },
  computed: {
    headers() {
      return {
        'X-Litemall-Admin-Token': getToken()
      }
    },
    attributesData() {
      var attributesData = []
      for (var i = 0; i < this.attributes.length; i++) {
        if (this.attributes[i].deleted) {
          continue
        }
        attributesData.push(this.attributes[i])
      }
      return attributesData
    }
  },
  created() {
    this.init()
  },
  methods: {
    init: function() {
      if (this.$route.query.id == null) {
        return
      }

      const goodsId = this.$route.query.id
      detailGoods(goodsId).then(response => {
        this.goods = response.data.data.goods
        // 稍微调整一下前后端不一致
        if (this.goods.brandId === 0) {
          this.goods.brandId = null
        }
        if (this.goods.keywords === '') {
          this.goods.keywords = null
        }
        this.specifications = response.data.data.specifications
        this.products = response.data.data.products
        this.attributes = response.data.data.attributes
        this.categoryIds = response.data.data.categoryIds

        this.galleryFileList = []
        for (var i = 0; i < this.goods.gallery.length; i++) {
          this.galleryFileList.push({
            url: this.goods.gallery[i]
          })
        }
        const keywords = response.data.data.goods.keywords
        if (keywords !== null) {
          this.keywords = keywords.split(',')
        }
      })

      listCatAndBrand().then(response => {
        this.categoryList = response.data.data.categoryList
        this.brandList = response.data.data.brandList
      })
    },
    handleCategoryChange(value) {
      this.goods.categoryId = value[value.length - 1]
    },
    handleCancel: function() {
      this.$store.dispatch('tagsView/delView', this.$route)
      this.$router.push({ path: '/resource/list' })
    },
    handleEdit: function() {
      const finalGoods = {
        goods: this.goods,
        specifications: this.specifications,
        products: this.products,
        attributes: this.attributes
      }
      editGoods(finalGoods)
        .then(response => {
          this.$notify.success({
            title: '成功',
            message: '编辑成功'
          })
          this.$store.dispatch('tagsView/delView', this.$route)
          this.$router.push({ path: '/resource/list' })
        })
        .catch(response => {
          MessageBox.alert('业务错误：' + response.data.errmsg, '警告', {
            confirmButtonText: '确定',
            type: 'error'
          })
        })
    },
    handleClose(tag) {
      this.keywords.splice(this.keywords.indexOf(tag), 1)
      this.goods.keywords = this.keywords.toString()
    },
    showInput() {
      this.newKeywordVisible = true
      this.$nextTick(_ => {
        this.$refs.newKeywordInput.$refs.input.focus()
      })
    },
    handleInputConfirm() {
      const newKeyword = this.newKeyword
      if (newKeyword) {
        this.keywords.push(newKeyword)
        this.goods.keywords = this.keywords.toString()
      }
      this.newKeywordVisible = false
      this.newKeyword = ''
    },
    uploadPicUrl: function(response) {
      this.goods.picUrl = response.data.url
    },
    uploadOverrun: function() {
      this.$message({
        type: 'error',
        message: '上传文件个数超出限制!最多上传5张图片!'
      })
    },
    handleGalleryUrl(response, file, fileList) {
      if (response.errno === 0) {
        this.goods.gallery.push(response.data.url)
      }
    },
    handleRemove: function(file, fileList) {
      for (var i = 0; i < this.goods.gallery.length; i++) {
        // 这里存在两种情况
        // 1. 如果所删除图片是刚刚上传的图片，那么图片地址是file.response.data.url
        //    此时的file.url虽然存在，但是是本机地址，而不是远程地址。
        // 2. 如果所删除图片是后台返回的已有图片，那么图片地址是file.url
        var url
        if (file.response === undefined) {
          url = file.url
        } else {
          url = file.response.data.url
        }

        if (this.goods.gallery[i] === url) {
          this.goods.gallery.splice(i, 1)
        }
      }
    },
    specChanged: function(label) {
      if (label === false) {
        this.specifications = [
          { specification: '规格', value: '标准', picUrl: '' }
        ]
        this.products = [
          { id: 0, specifications: ['标准'], price: 0.0, number: 0, url: '' }
        ]
      } else {
        this.specifications = []
        this.products = []
      }
    },
    uploadSpecPicUrl: function(response) {
      this.specForm.picUrl = response.data.url
    },
    handleSpecificationShow(row) {
      this.specForm = Object.assign({}, row)
      this.specVisiable = true
    },
    handleSpecificationEdit() {
      this.specForm.updateTime = ''
      for (var i = 0; i < this.specifications.length; i++) {
        const v = this.specifications[i]
        if (v.id === this.specForm.id) {
          this.specifications.splice(i, 1, this.specForm)
          break
        }
      }
      this.specVisiable = false
    },
    handleProductShow(row) {
      this.productForm = Object.assign({}, row)
      this.productVisiable = true
    },
    uploadProductUrl: function(response) {
      this.productForm.url = response.data.url
    },
    handleProductEdit() {
      this.productForm.updateTime = ''
      for (var i = 0; i < this.products.length; i++) {
        const v = this.products[i]
        if (v.id === this.productForm.id) {
          this.products.splice(i, 1, this.productForm)
          break
        }
      }
      this.productVisiable = false
    },
    handleAttributeShow(row) {
      if (row.id) {
        this.attributeForm = Object.assign({}, row)
        this.attributeAdd = false
      } else {
        this.attributeForm = {}
        this.attributeAdd = true
      }
      this.attributeVisiable = true
    },
    handleAttributeAdd() {
      this.attributes.unshift(this.attributeForm)
      this.attributeVisiable = false
    },
    handleAttributeEdit() {
      // 这是一个trick，设置updateTime的值为空，告诉后端这个记录已编辑需要更新。
      this.attributeForm.updateTime = ''
      for (var i = 0; i < this.attributes.length; i++) {
        const v = this.attributes[i]
        if (v.id === this.attributeForm.id) {
          this.attributes.splice(i, 1, this.attributeForm)
          break
        }
      }
      this.attributeVisiable = false
    },
    handleAttributeDelete(row) {
      row.deleted = true
    }
  }
}
</script>
