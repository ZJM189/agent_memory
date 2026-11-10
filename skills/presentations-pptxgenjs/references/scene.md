# JSON scene format

All coordinates are inches; `fontSize` is points. JSON paths are relative to the scene file. UTF-8 BOM is accepted. Set a real locally installed font. Element array order controls stacking. The builder supports the following subset of PptxGenJS; use a direct script for other features.

```json
{
  "width": 13.333333, "height": 7.5,
  "title": "Demonstration", "author": "Example",
  "fontFace": "Microsoft YaHei",
  "slides": [{
    "background": "EFF8FF",
    "notes": "Example data, not production evidence.",
    "elements": [
      {"type":"shape", "shape":"roundRect", "x":0.4,"y":0.4,"w":12.5,"h":0.8,
       "fill":"0878D8", "line":{"color":"0878D8","width":1}},
      {"type":"text", "text":"Editable title", "x":0.6,"y":0.5,"w":12,"h":0.5,
       "fontSize":28,"bold":true,"color":"FFFFFF", "align":"center"},
      {"type":"image", "path":"assets/icon.png", "x":0.6,"y":1.5,"w":0.7,"h":0.7},
      {"type":"line", "x":1.5,"y":2,"w":3,"h":0,"color":"0878D8","width":2,"endArrowType":"triangle"},
      {"type":"table", "rows":[["Item","Value"],["A","4"]], "x":0.6,"y":3,"w":4,"h":1,
       "options":{"fontSize":16,"border":{"color":"B9D8F0","pt":1}}},
      {"type":"chart", "chartType":"bar", "x":6,"y":2,"w":6,"h":4,
       "series":[{"name":"Records","labels":["Sep","Oct","Nov"],"values":[4,70,30]}],
       "options":{"barDir":"col","catAxisLabelFontSize":14,"valAxisLabelFontSize":12,
       "showLegend":false,"showValue":true,"chartColors":["0878D8"],"valAxisMaxVal":80}}
    ]
  }]
}
```

Text supports `fontFace`, `fontSize`, `bold`, `italic`, `color`, `align`, `valign`, `margin`, `breakLine`, `paraSpaceAfterPt`, `transparency`, `charSpacing`, `lineSpacingMultiple`. Default margin is zero, wrap is enabled, vertical alignment is middle, and shrink fitting is disabled; size your boxes properly. A text element is one editable text box. For multi-color phrases, use multiple boxes or direct PptxGenJS rich text.

Shapes support `rect`, `roundRect`, `ellipse`, `chevron`, `rightArrow`, `downArrow`, `upArrow` using PptxGenJS shape names. Set `fill` and `line` to color strings or full PptxGenJS option objects; `fill:"none"` / `line:"none"` means transparent.

Images are local file paths. Their explicit box stretches the image; preserve aspect ratio when defining dimensions, or pre-crop the source. The renderer rejects missing assets. Transparent PNGs preserve their alpha channel.

Chart `options` and table `options` pass to PptxGenJS; do not override element positions there. Native charts retain their embedded editable data. `showValue:true` enables labels, but use an independent visual check to confirm the chart's rendered result.

The builder validates finite non-negative positions and the canvas bounds, and chart arrays/value types. It cannot infer intentional overlap, font availability, semantic accuracy or glyph fit. Diagnose those through visual rendering.
