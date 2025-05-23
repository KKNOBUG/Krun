<template>
  <AppPage>
    <n-card>
      <template #header>
        <strong>Json解析</strong>
        <n-button plain type="primary" size="tiny" class="ml10" @click="beautifyJson">格式化</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="compressJson">压缩</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="escapeJson">转义</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="unEscapeJson">去除转义</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="chToUnicode">中文转Unicode</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="unicodeToCh">Unicode转中文</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="chToEn">中文逗号转英文逗号</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="foldAll">折叠</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="unfoldAll">展开</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="copy">复制</n-button>
        <n-button plain type="primary" size="tiny" class="ml10" @click="jsonDiff">比对</n-button>
      </template>
    </n-card>

    <monaco-editor :lang="'json'"
                   ref="monacoEditorRef"
                   :is-diff="isDiff"
                   :readOnly="false"
                   :theme="'vs-dark'"
                   v-model:value="jsonData">
    </monaco-editor>

  </AppPage>
</template>
<script setup name="textAnalysis">
import AppPage from "@/components/page/AppPage.vue";


const jsonData = ref('')
const monacoEditorRef = ref(null)
const isDiff = ref(false)

const beautifyJson = () => {
  if (!jsonData.value) return
  try {
    setValue(JSON.stringify(JSON.parse(jsonData.value), null, 4))
  } catch (e) {
    $message.warning('JSON格式错误')
  }
}

// 压缩Json
const compressJson = () => {
  if (!jsonData.value) return
  try {
    setValue(JSON.stringify(JSON.parse(jsonData.value)))
  } catch (e) {
    $message.warning('JSON格式错误')
  }
}

const escapeJson = () => {
  if (!jsonData.value) return
  try {
    setValue(jsonData.value.replace(/\r\n/g, '').replace(/"/g, '\\"'))
  } catch (e) {
    $message.warning('JSON格式错误')
  }
}

const unEscapeJson = () => {
  if (!jsonData.value) return
  try {
    setValue(jsonData.value.replace(/\\"/g, '"'))
  } catch (e) {
    $message.warning('JSON格式错误')
  }
}

const unicodeToCh = () => {
  if (!jsonData.value) return
  // 控制循环跃迁
  const str = jsonData.value;
  let len = 1;
  let result = '';
  // 注意，这里循环变量的变化是i=i+len 了
  for (let i = 0; i < str.length; i = i + len) {
    len = 1;
    let temp = str.charAt(i);
    if (temp === '\\') {
      // 找到形如 \u 的字符序列
      if (str.charAt(i + 1) === 'u') {
        // 提取从i+2开始(包括)的 四个字符
        const unicode = str.substring((i + 2), (i + 2) + 4);
        // 以16进制为基数解析unicode字符串，得到一个10进制的数字
        result += String.fromCharCode(parseInt(unicode, 16).toString(10));
        // 提取这个unicode经过了5个字符， 去掉这5次循环
        len = 6;
      } else {
        result += temp;
      }
    } else {
      result += temp;
    }
  }
  setValue(result)
  // return result;
}

// 把字符串中的汉字转换成Unicode
const chToUnicode = () => {
  if (!jsonData.value) return

  function isChinese(s) {
    return /[\u4e00-\u9fa5]/.test(s);
  }

  let str = jsonData.value;
  let unicode = '';
  for (let i = 0; i < str.length; i++) {
    const temp = str.charAt(i);
    if (isChinese(temp)) {
      unicode += '\\u' + temp.charCodeAt(0).toString(16);
    } else {
      unicode += temp;
    }
  }
  setValue(unicode)
}


const chToEn = () => {
  if (!jsonData.value) return
  setValue(jsonData.value.replace(/，/g, ','))
}

const foldAll = () => {
  monacoEditorRef.value.foldAll()
}

const unfoldAll = () => {
  monacoEditorRef.value.unfoldAll()
}

const copy = () => {
  if (!jsonData.value) {
    $message.warning('没有可复制的内容 👻')
    return
  }
  commonFunction().copyText(jsonData.value)
  $message.success('复制成功 🎉')
}

const jsonDiff = () => {
  isDiff.value = !isDiff.value
}

const setValue = (value) => {
  monacoEditorRef.value.setValue(value)
}
</script>

<style lang="scss" scoped>
.json-header {
  height: 80px;
}

.json-box {
  height: calc(100% - 80px);

  .monaco-box {
    padding: 20px;
  }
}

:deep(.el-card__body) {
  height: 95%;
}
</style>
