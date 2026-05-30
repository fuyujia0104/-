# 示例文件

本目录包含城市感官探索家项目的示例文件。

## 文件说明

### sample_area.geojson
这是一个示例的GeoJSON文件，展示了北京市南锣鼓巷及其周边区域的地理数据。

文件包含：
- 一个多边形区域，表示南锣鼓巷区域
- 两个点要素，表示南锣鼓巷中心和什刹海区域

## 使用方法

您可以使用`/api/import_map`端点导入此GeoJSON文件，对指定区域进行感官特征分析。

示例请求：
```bash
curl -X POST "http://localhost:8000/api/import_map"   -H "Content-Type: multipart/form-data"   -F "file=@sample_area.geojson"
```

## 自定义GeoJSON文件

您可以创建自己的GeoJSON文件，用于导入和分析不同的区域。GeoJSON文件应遵循以下格式：

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [经度1, 纬度1],
            [经度2, 纬度2],
            [经度3, 纬度3],
            [经度4, 纬度4],
            [经度1, 纬度1]
          ]
        ]
      },
      "properties": {
        "name": "区域名称",
        "description": "区域描述"
      }
    }
  ]
}
```

注意：
- 坐标顺序为[经度, 纬度]
- 多边形区域的最后一个坐标应与第一个坐标相同，以闭合区域
- properties对象可以包含自定义属性
