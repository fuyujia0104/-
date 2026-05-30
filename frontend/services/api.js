// 城市感官探索家 - API服务

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * 探索某个地点的感官画像
 * @param {number} lat - 纬度
 * @param {number} lon - 经度
 * @param {string} address - 地址（可选）
 * @returns {Promise} - 返回地点感官画像数据
 */
async function exploreLocation(lat, lon, address = null) {
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lon', lon);
    if (address) {
        params.append('address', address);
    }

    const response = await fetch(`${API_BASE_URL}/explore?${params}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

/**
 * 根据感官偏好搜索地点
 * @param {number} lat - 纬度
 * @param {number} lon - 经度
 * @param {string} preferences - 感官偏好
 * @param {number} radius - 搜索半径（公里）
 * @returns {Promise} - 返回搜索结果
 */
async function searchByPreferences(lat, lon, preferences, radius = 5) {
    const params = new URLSearchParams();
    params.append('lat', lat);
    params.append('lon', lon);
    params.append('preferences', preferences);
    params.append('radius', radius);

    const response = await fetch(`${API_BASE_URL}/search?${params}`);
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

/**
 * 添加用户感官标记
 * @param {number} lat - 纬度
 * @param {number} lon - 经度
 * @param {string} mark - 感官标记
 * @param {string} type - 标记类型
 * @returns {Promise} - 返回标记结果
 */
async function addSensoryMark(lat, lon, mark, type) {
    const response = await fetch(`${API_BASE_URL}/mark`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            lat,
            lon,
            mark,
            type
        }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

// 导出API函数
export {
    exploreLocation,
    searchByPreferences,
    addSensoryMark
};
