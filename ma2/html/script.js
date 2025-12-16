const cat_url = "http://8.131.145.185/api/cat";
const cat_item = "http://8.131.145.185/api/cat_items";
const item_detail = "http://8.131.145.185/api/item_detail";
const city_url = "http://8.131.145.185/api/data"

// 省份和城市数据（将从接口获取）
let locationData = [];
let locationDataMap = {}

// 模拟从API获取分类数据
function fetchCategories() {
    return fetch(cat_url)
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(data => {
            // 假设接口返回的数据格式为数组，包含id和name属性
            // 例如: [{id: 1, name: "红色系"}, {id: 2, name: "黄色系"}]
            return data;
        })
        .catch(error => {
            console.error('获取分类数据失败:', error);
            // 如果接口失败，使用默认数据
            return [
                {id: 1, name: "红色系"},
                {id: 2, name: "黄色系"}
            ];
        });
}

// 从接口获取省份数据
function fetchProvinces() {
    return fetch(city_url)
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(data => {
            locationData = data;
            return data;
        })
        .catch(error => {
            console.error('获取省份数据失败:', error);
            // 如果接口失败，使用默认数据
            locationData = [
                {
                    "name": "江苏省",
                    "cities": [
                        "南京市",
                        "无锡市",
                        "苏州市",
                        "南通市",
                        "徐州市",
                        "常州市",
                        "镇江市",
                        "扬州市",
                        "盐城市",
                        "淮安市",
                        "连云港市",
                        "宿迁市"
                    ]
                }];
            return locationData;
        });
}

// 模拟从API获取图片组数据
function fetchPhotoGroups(categoryId, date = null, province = null, city = null, size = null) {
    url = cat_item + "?cat=" + categoryId
    if (date != null) {
        url = url + "&date=" + date
        url = url + "&province=" + province
        url = url + "&city=" + city
        url = url + "&size=" + size
    }
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            return data;
        })
}

// 模拟从API获取图片组详情数据
function fetchGroupDetail(groupId) {
    return fetch(item_detail + "?id=" + groupId)
        .then(response => {
            if (!response.ok) {
                throw new Error('网络响应不正常');
            }
            return response.json();
        })
        .then(data => {
            console.log(data)
            return data;
        })
}

// DOM元素
const categoriesEl = document.getElementById('categories');
const photosGridEl = document.getElementById('photosGrid');
const loadingEl = document.getElementById('loading');
const emptyStateEl = document.getElementById('emptyState');
const detailContainerEl = document.getElementById('detailContainer');
const detailTitleEl = document.getElementById('detailTitle');
const detailGridEl = document.getElementById('detailGrid');
const backButtonEl = document.getElementById('backButton');
const scrollHintEl = document.getElementById('scrollHint');
const floatingFilterEl = document.getElementById('floatingFilter');
const filterButtonEl = document.getElementById('filterButton');
const filterModalEl = document.getElementById('filterModal');
const filterCancelEl = document.getElementById('filterCancel');
const filterApplyEl = document.getElementById('filterApply');
const dateInputEl = document.getElementById('dateInput');
const provinceSelectEl = document.getElementById('provinceSelect');
const citySelectEl = document.getElementById('citySelect');
const sizeSelectEl = document.getElementById('sizeSelect'); // 新增尺码下拉框
const filterSelectionEl = document.getElementById('filterSelection');
const detailFooterEl = document.getElementById('detailFooter');
const footerContentEl = document.getElementById('footerContent');

// 应用状态
let currentCategoryId = 1;
let categories = [];
let photoGroups = [];
let currentGroupDetail = null;
let currentFilter = {
    date: null,
    province: null,
    city: null,
    size: null
};

// 初始化应用
async function initApp() {
    try {
        // 获取分类数据
        categories = await fetchCategories();
        renderCategories();

        // 从接口获取省份数据
        await fetchProvinces();

        // 初始化省份选择器
        initProvinceSelect();

        // 默认加载第一个分类的图片组
        await loadCategoryGroups(currentCategoryId);

        // 检查是否需要显示滑动提示
        checkScrollHint();

        // 更新筛选结果显示
        updateFilterSelection();
    } catch (error) {
        console.error('初始化应用失败:', error);
        loadingEl.textContent = '加载失败，请刷新页面重试';
    }
}

// 初始化省份选择器
function initProvinceSelect() {
    provinceSelectEl.innerHTML = '<option value="">请选择省份</option>';

    locationData.forEach(province => {
        const option = document.createElement('option');
        option.value = province.name;
        option.textContent = province.name;
        locationDataMap[province.name] = province.cities
        provinceSelectEl.appendChild(option);
    });
}

// 更新城市选择器
function updateCitySelect(province) {
    citySelectEl.innerHTML = '<option value="">请选择城市</option>';

    if (!province) {
        citySelectEl.disabled = true;
        return;
    }

    const cities = locationDataMap[province] || [];

    cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        citySelectEl.appendChild(option);
    });

    citySelectEl.disabled = false;
}

// 更新筛选结果显示
function updateFilterSelection() {
    let selectionText = "请选择日期、地区和尺码";

    if (currentFilter.date || currentFilter.city || currentFilter.size) {
        selectionText = "";

        if (currentFilter.date) {
            // 格式化日期显示
            const date = new Date(currentFilter.date);
            const formattedDate = `${date.getMonth() + 1}月${date.getDate()}日`;
            selectionText += formattedDate;
        }

        if (currentFilter.city) {
            if (selectionText) selectionText += " | ";

            // 如果是直辖市，只显示城市名
            const isMunicipality = ['北京市', '上海市', '天津市', '重庆市'].includes(currentFilter.province);
            if (isMunicipality) {
                selectionText += currentFilter.city.replace('市', '');
            } else {
                selectionText += `${currentFilter.province} ${currentFilter.city}`;
            }
        }

        if (currentFilter.size) {
            if (selectionText) selectionText += " | ";
            selectionText += `尺码: ${currentFilter.size}`;
        }
    }

    filterSelectionEl.textContent = selectionText;
}

// 渲染分类标签
function renderCategories() {
    categoriesEl.innerHTML = '';
    categories.forEach(category => {
        if (currentCategoryId == "1") {
            currentCategoryId = category.id
        }
        const categoryEl = document.createElement('div');
        categoryEl.className = `category-item ${category.id === currentCategoryId ? 'active' : ''}`;
        categoryEl.dataset.id = category.id;

        // 创建分类图标
        const iconEl = document.createElement('div');
        iconEl.className = 'category-icon';

        const iconImg = document.createElement('img');
        iconImg.src = category.img;
        iconImg.alt = category.name;

        iconEl.appendChild(iconImg);

        // 创建分类名称
        const nameEl = document.createElement('span');
        nameEl.textContent = category.name;

        categoryEl.appendChild(iconEl);
        categoryEl.appendChild(nameEl);

        categoryEl.addEventListener('click', () => {
            if (category.id !== currentCategoryId) {
                currentCategoryId = category.id;
                renderCategories(); // 重新渲染分类以更新激活状态
                loadCategoryGroups(currentCategoryId);
            }
        });

        categoriesEl.appendChild(categoryEl);
    });
}

// 检查是否需要显示滑动提示
function checkScrollHint() {
    // 使用setTimeout确保DOM已渲染完成
    setTimeout(() => {
        const containerWidth = categoriesEl.parentElement.offsetWidth;
        const contentWidth = categoriesEl.scrollWidth;

        if (contentWidth > containerWidth) {
            scrollHintEl.style.display = 'flex';
        } else {
            scrollHintEl.style.display = 'none';
        }
    }, 100);
}

// 加载分类图片组
async function loadCategoryGroups(categoryId) {
    // 显示加载状态
    loadingEl.style.display = 'block';
    photosGridEl.style.display = 'none';
    emptyStateEl.style.display = 'none';

    try {
        photoGroups = await fetchPhotoGroups(
            categoryId,
            currentFilter.date,
            currentFilter.province,
            currentFilter.city,
            currentFilter.size
        );
        console.log(photoGroups)
        renderPhotoGroups();
    } catch (error) {
        console.error('加载图片组失败:', error);
        photosGridEl.innerHTML = '<div class="empty-state">加载失败，请重试</div>';
        photosGridEl.style.display = 'block';
    } finally {
        loadingEl.style.display = 'none';
    }
}

// 渲染图片组
function renderPhotoGroups() {
    photosGridEl.innerHTML = '';

    if (photoGroups.length === 0) {
        emptyStateEl.style.display = 'block';
        return;
    }

    photosGridEl.style.display = 'grid';

    photoGroups.forEach(group => {
        const groupEl = document.createElement('div');
        groupEl.className = 'photo-group';
        groupEl.dataset.id = group.id;

        // 创建图片容器
        const imageEl = document.createElement('div');
        imageEl.className = 'group-image';

        const img = document.createElement('img');
        // 使用第一张图片作为首图
        img.src = group.img;
        img.alt = `${group.name} 首图`;
        img.loading = 'lazy';

        imageEl.appendChild(img);

        // 创建组名称
        const nameEl = document.createElement('div');
        nameEl.className = 'group-name';
        nameEl.textContent = group.name;

        groupEl.appendChild(imageEl);
        groupEl.appendChild(nameEl);

        // 点击图片组跳转到详情页
        groupEl.addEventListener('click', () => {
            showGroupDetail(group.id, group.name);
        });

        photosGridEl.appendChild(groupEl);
    });
}

// 显示图片组详情
async function showGroupDetail(groupId, groupName) {
    try {
        // 显示加载状态
        detailTitleEl.textContent = '加载中...';
        detailGridEl.innerHTML = '';
        detailContainerEl.style.display = 'block';

        // 获取组详情数据
        currentGroupDetail = await fetchGroupDetail(groupId);

        // 获取底部悬浮框内容
        const footerContent = currentGroupDetail[0].text;

        // 更新详情页标题
        detailTitleEl.textContent = footerContent;

        // 渲染详情页图片
        renderGroupDetailImages();

        // // 更新底部悬浮框内容并显示
        updateDetailFooter(footerContent);

    } catch (error) {
        console.error('加载组详情失败:', error);
        detailGridEl.innerHTML = '<div class="empty-state">加载失败，请重试</div>';
    }
}

// 渲染组详情图片
function renderGroupDetailImages() {
    detailGridEl.innerHTML = '';

    if (currentGroupDetail.length === 0) {
        detailGridEl.innerHTML = '<div class="empty-state">该组暂无图片</div>';
        return;
    }

    currentGroupDetail.forEach(image => {
        const imageEl = document.createElement('div');
        imageEl.className = 'detail-image';

        const img = document.createElement('img');
        img.src = image.url;
        img.alt = image.title;

        imageEl.appendChild(img);
        detailGridEl.appendChild(imageEl);
    });
}

// 更新详情页底部悬浮框内容
function updateDetailFooter(content) {
    footerContentEl.textContent = content;
    detailFooterEl.style.display = 'block';
}

// 返回主页面
function backToHome() {
    detailContainerEl.style.display = 'none';
    // 隐藏底部悬浮框
    detailFooterEl.style.display = 'none';
}

// 显示筛选弹窗
function showFilterModal() {
    // 设置默认值
    if (currentFilter.date) {
        dateInputEl.value = currentFilter.date;
    } else {
        dateInputEl.value = '';
    }

    if (currentFilter.province) {
        provinceSelectEl.value = currentFilter.province;
        updateCitySelect(currentFilter.province);

        if (currentFilter.city) {
            citySelectEl.value = currentFilter.city;
        } else {
            citySelectEl.value = '';
        }
    } else {
        provinceSelectEl.value = '';
        citySelectEl.innerHTML = '<option value="">请先选择省份</option>';
        citySelectEl.disabled = true;
    }

    // 设置尺码选择状态
    if (currentFilter.size) {
        sizeSelectEl.value = currentFilter.size;
    } else {
        sizeSelectEl.value = '';
    }

    filterModalEl.style.display = 'flex';
}

// 隐藏筛选弹窗
function hideFilterModal() {
    filterModalEl.style.display = 'none';
}

// 应用筛选条件
function applyFilter() {
    const date = dateInputEl.value;
    const province = provinceSelectEl.value;
    const city = citySelectEl.value;
    const size = sizeSelectEl.value; // 从下拉框获取尺码

    currentFilter = {
        date: date || null,
        province: province || null,
        city: city || null,
        size: size || null
    };

    // 更新筛选结果显示
    updateFilterSelection();

    // 重新加载当前分类的图片
    loadCategoryGroups(currentCategoryId);

    // 隐藏弹窗
    hideFilterModal();
}

// 重置筛选条件
function resetFilter() {
    dateInputEl.value = '';
    provinceSelectEl.value = '';
    citySelectEl.innerHTML = '<option value="">请先选择省份</option>';
    citySelectEl.disabled = true;
    sizeSelectEl.value = ''; // 重置尺码选择

    currentFilter = {
        date: null,
        province: null,
        city: null,
        size: null
    };

    // 更新筛选结果显示
    updateFilterSelection();

    // 重新加载当前分类的图片
    loadCategoryGroups(currentCategoryId);

    // 隐藏弹窗
    hideFilterModal();
}

// 绑定事件监听器
backButtonEl.addEventListener('click', backToHome);
filterButtonEl.addEventListener('click', showFilterModal);
filterCancelEl.addEventListener('click', resetFilter);
filterApplyEl.addEventListener('click', applyFilter);

// 省份选择变化时更新城市列表
provinceSelectEl.addEventListener('change', function () {
    updateCitySelect(this.value);
});

// 监听窗口大小变化，更新滑动提示
window.addEventListener('resize', checkScrollHint);
// 启动应用
initApp();