<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { createStrategy, getStrategy, updateStrategy } from '../api/strategies'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const saving = ref(false)

const strategyid = ref('')
const contentText = ref('')

const isNew = computed(() => route.name === 'StrategyNew')

function initialContentText() {
  // content 字段结构你后续再细化；MVP 先保证能往返保存。
  return JSON.stringify({}, null, 2)
}

async function loadIfEdit() {
  if (isNew.value) {
    strategyid.value = ''
    contentText.value = initialContentText()
    return
  }

  const sid = route.params.strategyid
  if (typeof sid !== 'string' || !sid) {
    ElMessage.error('参数错误：strategyid')
    return
  }

  loading.value = true
  try {
    const res = await getStrategy(sid)
    strategyid.value = res.strategyid
    contentText.value = JSON.stringify(res.content ?? {}, null, 2)
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || e?.message || '加载策略失败')
  } finally {
    loading.value = false
  }
}

function parseContent(): any {
  try {
    return JSON.parse(contentText.value)
  } catch (e: any) {
    throw new Error('content 不是合法 JSON：' + (e?.message || String(e)))
  }
}

async function onSave() {
  if (!strategyid.value.trim()) {
    ElMessage.error('请填写 strategyid')
    return
  }

  let content: any
  try {
    content = parseContent()
  } catch (e: any) {
    ElMessage.error(e?.message || 'content JSON 校验失败')
    return
  }

  saving.value = true
  try {
    if (isNew.value) {
      await createStrategy({ strategyid: strategyid.value.trim(), content })
      ElMessage.success('创建成功')
    } else {
      const sid = route.params.strategyid
      if (typeof sid !== 'string') {
        ElMessage.error('参数错误：strategyid')
        return
      }
      await updateStrategy(sid, { strategyid: sid, content })
      ElMessage.success('保存成功')
    }

    router.push({ name: 'Strategies' })
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || e?.message || '保存失败')
  } finally {
    saving.value = false
  }
}

function onCancel() {
  router.push({ name: 'Strategies' })
}

onMounted(loadIfEdit)
</script>

<template>
  <div style="padding: 20px">
    <el-card>
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px">
        <div style="font-size: 16px; font-weight: 600">
          {{ isNew ? '新建策略' : '编辑策略' }}
        </div>
        <div style="display: flex; gap: 8px">
          <el-button @click="onCancel" :disabled="saving">返回</el-button>
          <el-button type="primary" @click="onSave" :loading="saving" :disabled="loading">
            保存
          </el-button>
        </div>
      </div>

      <el-form label-width="120px">
        <el-form-item label="strategyid">
          <el-input v-model="strategyid" :disabled="!isNew" placeholder="例如：20260330" />
        </el-form-item>

        <el-form-item label="content(JSON)">
          <el-input
            v-model="contentText"
            type="textarea"
            :rows="22"
            placeholder='请输入 JSON 对象，例如：{ "name": "策略A" }'
          />
          <div style="color: #666; font-size: 12px; margin-top: 6px">
            说明：MVP 允许 content 任意结构。daily_record 也先由前端维护在 JSON 内。
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

