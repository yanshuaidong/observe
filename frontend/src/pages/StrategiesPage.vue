<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { deleteStrategy, listStrategies, type StrategyItem } from '../api/strategies'

const router = useRouter()

const loading = ref(false)
const items = ref<StrategyItem[]>([])

async function load() {
  loading.value = true
  try {
    const res = await listStrategies()
    items.value = res.items || []
  } catch (e: any) {
    ElMessage.error(e?.response?.data?.detail || e?.message || '加载策略失败')
  } finally {
    loading.value = false
  }
}

function strategyName(item: StrategyItem): string {
  return item?.content?.name || item.strategyid
}

async function onDelete(strategyid: string) {
  // 简化：不做二次确认对话框，避免你先实现逻辑再美化 UI。
  await deleteStrategy(strategyid)
  ElMessage.success('删除成功')
  await load()
}

function onEdit(strategyid: string) {
  router.push({ name: 'StrategyEdit', params: { strategyid } })
}

function onNew() {
  router.push({ name: 'StrategyNew' })
}

onMounted(load)
</script>

<template>
  <div style="padding: 20px">
    <el-card>
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px">
        <div>
          <div style="font-size: 16px; font-weight: 600">策略管理</div>
          <div style="color: #666; font-size: 12px; margin-top: 4px">MVP：只做 strategy CRUD（daily_record 在 content 内）</div>
        </div>
        <el-button type="primary" @click="onNew">新建策略</el-button>
      </div>

      <el-table v-loading="loading" :data="items" style="width: 100%">
        <el-table-column prop="strategyid" label="strategyid" width="180" />
        <el-table-column label="策略名称">
          <template #default="scope">
            {{ strategyName(scope.row as StrategyItem) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220">
          <template #default="scope">
            <div style="display: flex; gap: 8px">
              <el-button size="small" @click="onEdit((scope.row as StrategyItem).strategyid)">编辑</el-button>
              <el-button
                size="small"
                type="danger"
                @click="onDelete((scope.row as StrategyItem).strategyid)"
              >
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

