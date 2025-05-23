<template>
  <n-card :bordered="false" size="small">
    <!-- 标题行 -->
    <n-grid :cols="24" :x-gap="10" class="header-row">
      <n-gi :span="isFormDataAndForBody ? 2 : 8">
        <n-text strong v-if="isFormDataAndForBody">类型</n-text>
        <n-text strong v-else>变量</n-text>
      </n-gi>
      <n-gi :span="isFormDataAndForBody ? 6 : 0">
        <n-text strong v-if="isFormDataAndForBody">变量</n-text>
      </n-gi>
      <n-gi :span="8">
        <n-text strong>数据</n-text>
      </n-gi>
      <n-gi :span="6">
        <n-text strong>描述</n-text>
      </n-gi>
      <n-gi :span="2">
        <n-button @click="openBatchAddModal" type="primary" tertiary>
          批量
        </n-button>
      </n-gi>
    </n-grid>

    <!-- 数据行，使用 v-for 指令遍历 items 数组，为每个元素生成一行 -->
    <div v-for="(item, index) in items" :key="index" class="key-value-row">
      <n-grid :cols="24" :x-gap="10">
        <!-- Key 列，根据是否为 form-data 模式且是请求体部分，显示不同内容 -->
        <n-gi :span="isFormDataAndForBody ? 2 : 8">
          <!-- 如果不是 form-data 模式且是请求体部分，显示输入框用于输入变量名称 -->
          <n-space align="center" :wrap-item="false">
            <n-input
                v-if="!isFormDataAndForBody"
                v-model:value="item.key"
                placeholder="请输入变量名称"
                clearable
                style="flex: 1;"
            />
            <!-- 如果是 form-data 模式且是请求体部分，显示下拉选择框用于选择类型 -->
            <n-space v-else align="center" :wrap-item="false" style="flex: 1;">
              <n-select
                  v-model:value="item.type"
                  :options="[
                    { label: 'Text', value: 'text' },
                    { label: 'File', value: 'file' }
                  ]"
                  size="medium"
                  style="width: 80px; flex-shrink: 0;"
                  @update:value="(value) => handleTypeChange(value, index)"
              />
            </n-space>
          </n-space>
        </n-gi>
        <!-- 只有在 form-data 模式且是请求体部分时显示该列，显示输入框用于输入变量数据 -->
        <n-gi :span="isFormDataAndForBody ? 6 : 0">
          <n-input
              v-if="isFormDataAndForBody"
              v-model:value="item.key"
              placeholder="请输入变量数据"
              clearable
              style="flex: 1;"
          />
        </n-gi>

        <!-- Value列：根据类型显示不同内容 -->
        <n-gi :span="8">
          <!-- 如果不是 form-data 模式且是请求体部分或者类型为 text，显示输入框和关联数据按钮 -->
          <div v-if="!isFormDataAndForBody || item.type === 'text'" class="text-input-wrapper">
            <n-input
                v-model:value="item.value"
                placeholder="请输入变量数据"
                clearable
                style="flex: 1;"
            />
            <!-- 点击关联数据按钮，触发 handleDataAssociation 方法 -->
            <n-button
                circle
                tertiary
                type="primary"
                size="small"
                @click="handleDataAssociation(index)"
                class="join-button"
            >
              <template #icon>
                <TheIcon icon="material-symbols:dataset-linked-outline" :size="18"/>
              </template>
            </n-button>
          </div>
          <!-- 如果是 form-data 模式且是请求体部分并且类型为 file，显示文件上传按钮和清除文件按钮 -->
          <div v-else-if="isFormDataAndForBody && item.type === 'file'" class="file-upload-wrapper">
            <n-upload
                :show-file-list="false"
                @change="({ file }) => handleFileChange(file, index)"
                class="file-upload"
            >
              <n-button block class="upload-button">
                <template #icon>
                  <TheIcon icon="material-symbols:upload-file" :size="18"/>
                </template>
                <!-- 显示文件名，如果文件名过长会进行格式化处理 -->
                <span class="file-name">{{ formatFileName(item.value) }}</span>
              </n-button>
            </n-upload>
            <!-- 点击清除文件按钮，触发 handleClearFile 方法 -->
            <n-button
                circle
                tertiary
                type="primary"
                size="small"
                @click="handleClearFile(index)"
                class="join-button"
            >
              <template #icon>
                <TheIcon icon="ri:delete-bin-5-line" :size="18"/>
              </template>
            </n-button>
          </div>

        </n-gi>

        <!-- Description列 -->
        <n-gi :span="6">
          <n-input v-model:value="item.description" placeholder="请输入变量描述" clearable/>
        </n-gi>

        <!-- 删除列，显示“删除”按钮，点击后触发 handleRemove 方法 -->
        <n-gi :span="2">
          <n-button @click="handleRemove(index)" type="primary" tertiary>
            删除
          </n-button>
        </n-gi>
      </n-grid>
    </div>

    <!-- 操作行，显示“添加”按钮，点击后触发 handleAdd 方法 -->
    <div class="add-button-container">
      <n-button @click="handleAdd" type="primary" dashed block class="add-button">
        添加
      </n-button>
    </div>

    <!-- 批量添加模态框 -->
    <n-modal
        v-model:show="isBatchAddModalVisible"
        preset="dialog"
        :title="null"
        :show-icon="false"
        :header-style="{ display: 'none' }"
        positive-text="确认"
        @positive-click="handleBatchAdd"
        style="width: 600px;"
    >
      <n-input
          type="textarea"
          v-model:value="batchInput"
          placeholder="按 key:value:description 格式输入"
          :rows="10"
          style="min-height: 6rem; margin-bottom: 1rem;"
          resize="vertical"
      />
    </n-modal>

  </n-card>
</template>

<script setup>
import {computed, defineEmits, defineProps, ref} from 'vue';
import TheIcon from "@/components/icon/TheIcon.vue";


const props = defineProps({
  // 接收一个数组，包含键值对信息
  items: {
    type: Array,
    required: true
  },
  // 请求体类型，默认为 'none'
  bodyType: {
    type: String,
    default: 'none'
  },
  // 判断是否是请求体部分，默认为 false
  isForBody: {
    type: Boolean,
    default: false
  }
});
// 定义组件的自定义事件
const emit = defineEmits(['add', 'remove', 'update:items']);
// 控制批量添加模态框的显示与隐藏
const isBatchAddModalVisible = ref(false);
// 存储批量输入的内容
const batchInput = ref('');

// 计算是否为 form-data 模式且是请求体部分
const isFormDataAndForBody = computed(() => props.bodyType === 'form-data' && props.isForBody);

// 处理添加键值对的方法
const handleAdd = () => {
  // 创建一个新的键值对对象
  const newItems = [...props.items, {key: '', value: '', type: 'text'}];
  // 触发 update:items 事件，更新父组件的 items 数据
  emit('update:items', newItems);
  // 触发 add 事件
  emit('add');
};

// 处理删除键值对的方法
const handleRemove = (index) => {
  // 过滤掉要删除的键值对
  const newItems = props.items.filter((_, i) => i !== index);
  // 触发 update:items 事件，更新父组件的 items 数据
  emit('update:items', newItems);
  // 触发 remove 事件
  emit('remove', index);
};

// 打开批量添加模态框的方法
const openBatchAddModal = () => {
  $message.warning('该动作会覆盖原有Key-Value内容，请三思！');
  $message.warning('该动作会覆盖原有Key-Value内容，请三思！');
  $message.warning('该动作会覆盖原有Key-Value内容，请三思！');
  // 将当前的键值对信息格式化为 key:value:description 格式，填充到批量输入框中
  const nonEmptyItems = props.items.filter(item => item.key || item.value);
  batchInput.value = nonEmptyItems.map(item => {
    if (item.description) {
      return `${item.key}:${item.value}:${item.description}`;
    }
    return `${item.key}:${item.value}`;
  }).join('\n');
  isBatchAddModalVisible.value = true;
};

// 处理批量添加的方法
const handleBatchAdd = () => {
  const lines = batchInput.value.split('\n');
  const newItems = [];
  lines.forEach((line) => {
    const parts = line.split(':');
    if (parts.length === 2) {
      const key = parts[0].trim();
      const value = parts[1].trim();
      newItems.push({key, value, type: "text", description: ''});
    } else if (parts.length === 3) {
      const key = parts[0].trim();
      const value = parts[1].trim();
      const desc = parts[2].trim();
      newItems.push({key, value, type: "text", description: desc});
    }
  });
  emit('update:items', newItems);
  emit('add');
  isBatchAddModalVisible.value = false;
  batchInput.value = '';
};

// 处理文件选择的方法
const handleFileChange = (file, index) => {
  const newItems = [...props.items];
  // 更新指定索引的键值对的 value 为选择的文件
  newItems[index].value = file.file;
  emit('update:items', newItems);
};

// 处理清除文件的方法
const handleClearFile = (index) => {
  const newItems = [...props.items];
  // 将指定索引的键值对的 value 清空
  newItems[index].value = '';
  emit('update:items', newItems);
};

// 格式化文件名的方法，如果文件名过长，隐藏中间部分
const formatFileName = (file) => {
  if (!file) return '请选择上传文件';
  if (file instanceof File) {
    const name = file.name;
    if (name.length > 20) {
      const ext = name.split('.').pop();
      const nameWithoutExt = name.slice(0, -(ext.length + 1));
      const firstPart = nameWithoutExt.slice(0, 8);
      const lastPart = nameWithoutExt.slice(-8);
      return `${firstPart}...${lastPart}.${ext}`;
    }
    return name;
  }
  return '请选择上传文件';
};

// 处理类型变化的方法，当类型切换到 text 时，清空文件值
const handleTypeChange = (value, index) => {
  const newItems = [...props.items];
  newItems[index].type = value;
  if (value === 'text') {
    newItems[index].value = '';
  }
  emit('update:items', newItems);
};

// 处理数据关联的方法，点击关联数据按钮时触发
const handleDataAssociation = (index) => {
  // 这里可以添加数据关联的逻辑
  $message.warning(`点击了第 ${index} 项的数据关联按钮`)
  console.log(`点击了第 ${index} 项的数据关联按钮`);
};

</script>


<style scoped>
.key-value-row {
  margin-top: 10px;
}

.add-button-container {
  margin-top: 24px;
  padding: 0;
  width: 98.6%;
}

/* 确保文件上传按钮与垃圾桶在同一行 */
.file-upload-wrapper,
.text-input-wrapper {
  display: flex;
  align-items: center;
  gap: 5px;
  width: 100%;
}

/* 确保文件上传按钮与输入框宽度一致 */
.file-upload :deep(.n-upload-trigger) {
  width: 100%;
}

.upload-button:hover {
  border-color: #F4511E;
  color: #F4511E;
}

.upload-button:active {
  border-color: #0c7a43;
  color: #0c7a43;
}

/* 确保清除文件&关联数据图标不会移位 */
.join-button {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

</style>
