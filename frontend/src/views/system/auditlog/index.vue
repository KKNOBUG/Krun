<script setup>
import {h, onMounted, ref} from 'vue'
import {NInput, NSelect, NTag} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import api from '@/api'
import {formatDateTime} from "@/utils";

defineOptions({ name: '审计日志' })

const $table = ref(null)
const queryItems = ref({})

onMounted(() => {
  $table.value?.handleSearch()
})

function formatTimestamp(timestamp) {
  const date = new Date(timestamp)

  const pad = (num) => num.toString().padStart(2, '0')

  const year = date.getFullYear()
  const month = pad(date.getMonth() + 1) // 月份从0开始，所以需要+1
  const day = pad(date.getDate())
  const hours = pad(date.getHours())
  const minutes = pad(date.getMinutes())
  const seconds = pad(date.getSeconds())

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
}

// 获取当天的开始时间的时间戳
function getStartOfDayTimestamp() {
  const now = new Date()
  now.setHours(0, 0, 0, 0) // 将小时、分钟、秒和毫秒都设置为0
  return now.getTime()
}

// 获取当天的结束时间的时间戳
function getEndOfDayTimestamp() {
  const now = new Date()
  now.setHours(23, 59, 59, 999) // 将小时设置为23，分钟设置为59，秒设置为59，毫秒设置为999
  return now.getTime()
}

const startOfDayTimestamp = getStartOfDayTimestamp()
const endOfDayTimestamp = getEndOfDayTimestamp()

queryItems.value.start_time = formatTimestamp(startOfDayTimestamp)
queryItems.value.end_time = formatTimestamp(endOfDayTimestamp)

const datetimeRange = ref([startOfDayTimestamp, endOfDayTimestamp])
const handleDateRangeChange = (value) => {
  if (value == null) {
    queryItems.value.start_time = null
    queryItems.value.end_time = null
  } else {
    queryItems.value.start_time = formatTimestamp(value[0])
    queryItems.value.end_time = formatTimestamp(value[1])
  }
}

const methodOptions = [
  {
    label: 'GET',
    value: 'GET',
  },
  {
    label: 'POST',
    value: 'POST',
  },
  {
    label: 'PUT',
    value: 'PUT',
  },
  {
    label: 'DELETE',
    value: 'DELETE',
  },
]

const columns = [
  {
    title: '用户名称',
    key: 'username',
    width: '100px',
    align: 'center',
    ellipsis: { tooltip: true },
    render(row) {
      return h(NTag, {type: 'primary'}, {default: () => row.username})
    },
  },
  {
    title: '功能模块',
    key: 'request_tags',
    align: 'center',
    width: '150px',
    ellipsis: { tooltip: true },
    render(row) {
      return h(NTag, {type: 'info'}, {default: () => row.request_tags})
    },
  },
  {
    title: '接口概要',
    key: 'request_summary',
    align: 'center',
    width: '200px',
    ellipsis: { tooltip: true },
  },
  {
    title: '请求方法',
    key: 'request_method',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      return h(NTag, {type: 'info'}, {default: () => row.request_method})
    },
  },
  {
    title: '请求路由',
    key: 'request_router',
    align: 'center',
    width: '200px',
    ellipsis: { tooltip: true },
  },
  {
    title: '请求时间',
    key: 'request_time',
    align: 'center',
    width: '200px',
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', formatDateTime(row.request_time))
    },
  },
  {
    title: '请求来源',
    key: 'request_client',
    align: 'center',
    width: '150px',
    ellipsis: { tooltip: true },
  },
  {
    title: '请求头部',
    key: 'request_header',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', JSON.stringify(row.request_header, null, 2))
    },
  },
  {
    title: '请求参数',
    key: 'request_params',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      try {
        if (row.request_params === null) return;
        const parsed = JSON.parse(row.request_params);
        return h('span', JSON.stringify(parsed));
      } catch (error) {
        return h('span', row.request_params)
      }
    },
  },
  {
    title: '响应时间',
    key: 'response_time',
    align: 'center',
    width: '200px',
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', formatDateTime(row.response_time))
    },
  },
  {
    title: '响应头部',
    key: 'response_header',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', JSON.stringify(row.request_header, null, 2))
    },
  },
  {
    title: '响应代码',
    key: 'response_code',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      return h(NTag, {type: 'info'}, {default: () => row.response_code})
    },
  },
  {
    title: '响应信息',
    key: 'response_message',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
  },
  {
    title: '响应参数',
    key: 'response_params',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      return h('span', JSON.stringify(row.request_header, null, 2))
    },
  },
  {
    title: '响应耗时',
    key: 'response_elapsed',
    align: 'center',
    width: '100px',
    ellipsis: { tooltip: true },
    render(row) {
      return h(NTag, {type: 'primary'}, {default: () => row.response_elapsed})
    },
  }
]
</script>

<template>
  <!-- 业务页面 -->
  <CommonPage>
    <!-- 表格 -->
    <CrudTable
      ref="$table"
      v-model:query-items="queryItems"
      :columns="columns"
      :get-data="api.getAuditLogList"
      :single-line="true"
      :scroll-x="1800"
    >
      <template #queryBar>
        <QueryBarItem label="用户名称" :label-width="70">
          <NInput
            v-model:value="queryItems.username"
            clearable
            type="text"
            placeholder="请输入用户名称"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="功能模块" :label-width="70">
          <NInput
            v-model:value="queryItems.request_tags"
            clearable
            type="text"
            placeholder="请输入功能模块"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="接口概要" :label-width="70">
          <NInput
            v-model:value="queryItems.request_summary"
            clearable
            type="text"
            placeholder="请输入接口概要"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="请求方法" :label-width="70">
          <NSelect
            v-model:value="queryItems.request_method"
            style="width: 180px"
            :options="methodOptions"
            clearable
            placeholder="请选择请求方法"
          />
        </QueryBarItem>
        <QueryBarItem label="请求路由" :label-width="70">
          <NInput
            v-model:value="queryItems.request_router"
            clearable
            type="text"
            placeholder="请输入请求路由"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="响应代码" :label-width="60">
          <NInput
            v-model:value="queryItems.response_code"
            clearable
            type="text"
            placeholder="请输入响应代码"
            @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
        <QueryBarItem label="创建时间" :label-width="70">
          <NDatePicker
            v-model:value="datetimeRange"
            type="datetimerange"
            clearable
            placeholder="请选择时间范围"
            @update:value="handleDateRangeChange"
          />
        </QueryBarItem>
      </template>
    </CrudTable>
  </CommonPage>
</template>
