function loadDraft() {
  return fetch("draft.json").then(function (r) {return r.json()});
}
let draft;
window.addEventListener("load", function () {
  const container = document.querySelector(".container");
  loadDraft().then(function (_draft) {
    const draft = scaleDraft(_draft, 4);
    container.appendChild(textToFragment(draft, "Fatih Erikli", 50, 3, 10));
    container.appendChild(textToFragment(draft, `I am a software developer. I live in Karab${String.fromCharCode(252)}k. I am creating a 3d modeling software. Ben Fatih. Karab${String.fromCharCode(252)}k'te ya${String.fromCharCode(351)}${String.fromCharCode(305)}yorum. 3 boyutlu modelleme yaz${String.fromCharCode(305)}l${String.fromCharCode(305)}m${String.fromCharCode(305)} geli${String.fromCharCode(351)}tiriyorum.`, 30, 3, 6));
  });
});
function textToFragment(draft, text, txtheight, spaceinbetween, spacerwidth) {
  const fragment = document.createElement("div");
  fragment.style.display = "flex";
  fragment.style.flexDirection = "row";
  fragment.style.gap = `${spaceinbetween}px`;
  fragment.style.flexWrap = "wrap";
  let spacer = 0;
  let prev;
  for (const t of text) {
    if (t == " ") {
      spacer += spacerwidth;
      continue;
    }
    if (spacer > 0) {
      prev.style.marginRight = `${spacer}px`;
      spacer = 0;
    }
    if (t == "\n") {
      prev.style.flexBasis = "100%";
      continue;
    }
    const canvaswd = glyphToCanvas(draft, t);
    const rat = txtheight/canvaswd.height;
    canvaswd.canvasElement.style.width = `${canvaswd.width*rat}px`;
    canvaswd.canvasElement.style.height = `${canvaswd.height*rat}px`;
    fragment.appendChild(canvaswd.canvasElement);
    prev = canvaswd.canvasElement;
  }
  return fragment;
}
function glyphToCanvas(draft, glyph) {
  const glyphObjects = findGlyphGroup(draft, glyph);
  const boundingBox = boundingBoxObjects(glyphObjects);
  const origin = boundingBoxOrigin(boundingBox);
  const width = (boundingBox["max-x"] - boundingBox["min-x"]);
  const height = (boundingBox["max-y"] - boundingBox["min-y"]);
  const path2ds = [];
  for (const obj of glyphObjects) {
    if (obj["type"] == "curved-surface") {
      const points = []
      for (const point of obj["points"]) {
        const x = width/2 + (point["x"] - origin["x"]);
        const y = (height/2) + (point["y"] - origin["y"]) * -1;
        points.push([x, y]);
      }
      path2ds.push(createPath2dLerp(points));
    }
  }
  const canvasElement = createCanvasElement(width, height);
  const canvasContext = canvasElement.getContext("2d");
  canvasContext.fillStyle = "black";
  for (const path2d of path2ds) {
    canvasContext.fill(path2d);
  }
  return {canvasElement, width, height};
}
function getGroupContent(draft, groupId) {
  const groupContent = [];
  for (const obj of draft) {
    if ((obj.type == "ball" || obj.type == "curved-surface") && obj["group-id"] == groupId) {
      groupContent.push(obj);
    }
  }
  return groupContent;
}
function findGlyphGroup(draft, glyph) {
  for (const obj of draft) {
    if (obj.type == "glyph" && obj.glyph == glyph) {
      return getGroupContent(draft, obj["group-id"]);
    }
  }
  throw new Error(`Glyph not found: ${glyph}`);
}
function scaleDraft(draft, s) {
  const draftnew = [];
  for (const obj of draft) {
    if (obj.type == "ball") {
      draftnew.push({
        ...obj,
        x: obj.x * s,
        y: obj.y * s,
        z: obj.z * s,
      })
    } else if (obj.type == "curved-surface") {
      draftnew.push({
        ...obj,
        points: obj.points.map((point) => ({
          x: point.x * s,
          y: point.y * s,
          z: point.z * s
        }))
      });
    } else {
      draftnew.push(obj);
    }
  }
  return draftnew;
}
function renderTextCanvas(draft, text, dpi) {
  draft = scaleDraft(draft, dpi);
  const SPACE_WIDTH = 60 * dpi;
  const SPACE_INBETWEEN = 20 * dpi;
  let canvasWidth = 0;
  let canvasHeight = 0;
  let currentX = 0;
  let currentY = 0;
  const path2ds = [];
  let glyphheight;
  for (let i = 0; i < text.length; i++) {
    const glyph = text[i];
    if (glyph == " ") {
      canvasWidth += SPACE_WIDTH;
      currentX += SPACE_WIDTH;
      continue;
    }
    const glyphObjects = findGlyphGroup(draft, glyph);
    const boundingBox = boundingBoxObjects(glyphObjects);
    const origin = boundingBoxOrigin(boundingBox);
    const width = (boundingBox["max-x"] - boundingBox["min-x"]);
    const height = (boundingBox["max-y"] - boundingBox["min-y"]);
    if (typeof glyphheight == "undefined") {
      glyphheight = height;
      canvasHeight = height;
    }
    for (const obj of glyphObjects) {
      if (obj["type"] == "curved-surface") {
        const points = []
        for (const point of obj["points"]) {
          const x = currentX + width/2 + (point["x"] - origin["x"]);
          const y = currentY + (height/2) + (point["y"] - origin["y"]) * -1;
          points.push([x, y]);
        }
        path2ds.push(createPath2d(points));
      }
    }
    if (i < text.length - 1) {
      currentX += SPACE_INBETWEEN; 
    }
    canvasWidth = Math.max(canvasWidth, currentX + width);
    currentX += width;
  }
  const canvasElement = createCanvasElement(canvasWidth, canvasHeight);
  const canvasContext = canvasElement.getContext("2d");
  canvasContext.fillStyle = "black";
  canvasContext.strokeStyle = "black";
  for (const path2d of path2ds) {
    // canvasContext.fill(path2d);
    canvasContext.stroke(path2d);
  }
  return canvasElement;
}
function blurCanvas(canvasContext, canvasWidth, canvasHeight, square) {
  const imageData = canvasContext.getImageData(0, 0, canvasWidth, canvasHeight);
  const data = imageData.data;
  for (let x = 0; x < canvasWidth-square; x+= square) {
    for (let y = 0; y < canvasHeight-square; y += square) {
      const rgb = avgRGB(x, y, square, data, canvasWidth);
      
      for (let xx = x; xx < x + square; xx++) {
      for (let yy = y; yy < y + square; yy++) {
        const i = xyIndex(xx, yy, canvasWidth);
        data[i] = rgb[0];
        data[i+1] = rgb[1];
        data[i+2] = rgb[2];
      }}
    }
  }
  canvasContext.putImageData(imageData, 0, 0);
}
function avgRGB(x, y, square, imageData, imageWidth) {
  const r = []
  const g = []
  const b = []
  for (let xx = x; xx < x + square; xx++) {
    for (let yy = y; yy < y + square; yy++) {
      const i = xyIndex(xx, yy, imageWidth);
      r.push(imageData[i])
      g.push(imageData[i+1])
      b.push(imageData[i+2])
    }
  }
  return [avg(r), avg(g), avg(b)];
}
function avg(arr) {
  let sum = 0;
  for (const n of arr) {
    sum += n;
  }
  return sum / arr.length;
}
function xyIndex(x, y, width) {
  return y*width*4 + x*4
}
function renderTextSvg(text, scale) {
  const SPACE_WIDTH = 60;
  const SPACE_INBETWEEN = 20;
  let svgWidth = 0;
  let svgHeight = 0;
  let currentX = 0;
  const svgContent = [];
  for (const glyph of text) {
    if (glyph == " ") {
      svgWidth += SPACE_WIDTH;
      currentX += SPACE_WIDTH;
      continue;
    }
    const glyphObjects = findGlyphGroup(glyph);
    const boundingBox = boundingBoxObjects(glyphObjects);
    const origin = boundingBoxOrigin(boundingBox);
    const width = (boundingBox["max-x"] - boundingBox["min-x"]);
    const height = (boundingBox["max-y"] - boundingBox["min-y"]);
    svgHeight = Math.max(height, svgHeight);
    for (const obj of glyphObjects) {
      if (obj["type"] == "curved-surface") {
        const points = []
        for (const point of obj["points"]) {
          const x = currentX + width/2 + (point["x"] - origin["x"]);
          const y = (height/2) + (point["y"] - origin["y"]) * -1;
          points.push([x, y]);
        }
        svgContent.push(createPath(points));
      }
    }
    // const rect = createRect(currentX, 0, width, height);
    // svgContent.push(rect);
    svgWidth += width + SPACE_INBETWEEN;
    currentX += width + SPACE_INBETWEEN;
  }
  const svgElement = createSvgElement(svgWidth, svgHeight, scale);
  for (const svgContentElement of svgContent) {
    svgElement.appendChild(svgContentElement);
  }
  return svgElement;
}
function createCanvasElement(width, height) {
  const canvasElement = document.createElement("canvas");
  canvasElement.setAttribute("width", width);
  canvasElement.setAttribute("height", height);
  return canvasElement;
}
function createSvgElement(width, height, scale) {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", width*scale);
  svg.setAttribute("height", height*scale);
  svg.setAttribute("viewBox", `0, 0, ${width}, ${height}`);
  return svg;
}
function boundingBoxObjects(objects) {
  let minX, maxX, minY, maxY, minZ, maxZ;
  for (const obj of objects) {
    const boundingBox = objBoundingBox(obj);
    if (typeof minX == "undefined" || boundingBox["min-x"] < minX) {
      minX = boundingBox["min-x"];
    }
    if (typeof maxX == "undefined" || boundingBox["max-x"] > maxX) {
      maxX = boundingBox["max-x"];
    }
    if (typeof minY == "undefined" || boundingBox["min-y"] < minY) {
      minY = boundingBox["min-y"];
    }
    if (typeof maxY == "undefined" || boundingBox["max-y"] > maxY) {
      maxY = boundingBox["max-y"];
    }
    if (typeof minZ == "undefined" || boundingBox["min-z"] < minZ) {
      minZ = boundingBox["min-z"];
    }
    if (typeof maxZ == "undefined" || boundingBox["max-z"] > maxZ) {
      maxZ = boundingBox["max-z"];
    }
  }
  return {"min-x": minX, "max-x": maxX,
          "min-y": minY, "max-y": maxY,
          "min-z": minZ, "max-z": maxZ};
}
function objBoundingBox(obj) {
  if (obj["type"] == "ball") {
    return {"min-x": obj["x"], "max-x": obj["x"],
            "min-y": obj["y"], "max-y": obj["y"],
            "min-z": obj["z"], "max-z": obj["z"]};
  }
  if (obj["type"] == "curved-surface") {
    const bbox = {
      "min-x": undefined, "max-x": undefined,
      "min-y": undefined, "max-y": undefined,
      "min-z": undefined, "max-z": undefined,
    };
    for (const point of obj["points"]) {
      if (typeof bbox["min-x"] == "undefined" || point["x"] < bbox["min-x"]) {bbox["min-x"] = point["x"];}
      if (typeof bbox["max-x"] == "undefined" || point["x"] > bbox["max-x"]) {bbox["max-x"] = point["x"];}
      if (typeof bbox["min-y"] == "undefined" || point["y"] < bbox["min-y"]) {bbox["min-y"] = point["y"];}
      if (typeof bbox["max-y"] == "undefined" || point["y"] > bbox["max-y"]) {bbox["max-y"] = point["y"];}
      if (typeof bbox["min-z"] == "undefined" || point["z"] < bbox["min-z"]) {bbox["min-z"] = point["z"];}
      if (typeof bbox["max-z"] == "undefined" || point["z"] > bbox["max-z"]) {bbox["max-z"] = point["z"];}
    }
    return {
      "min-x": bbox["min-x"], "max-x": bbox["max-x"],
      "min-y": bbox["min-y"], "max-y": bbox["max-y"],
      "min-z": bbox["min-z"], "max-z": bbox["max-z"]
    };
  }
}
function boundingBoxOrigin(boundingBox) {
  return {
    "x": Math.floor((boundingBox["min-x"] + boundingBox["max-x"])/2),
    "y": Math.floor((boundingBox["min-y"] + boundingBox["max-y"])/2),
    "z": Math.floor((boundingBox["min-z"] + boundingBox["max-z"])/2)};
}
function createRect(x, y, width, height) {
  const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  rect.setAttribute("x", x);
  rect.setAttribute("y", y);
  rect.setAttribute("width", width);
  rect.setAttribute("height", height);
  rect.setAttribute("fill", "black");
  return rect;
}
function createCircle(x, y) {
  const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  circle.setAttribute("cx", x);
  circle.setAttribute("cy", y);
  circle.setAttribute("r", 3);
  circle.setAttribute("fill", "black");
  return circle;
}
function createPath2dLerp(points) {
  const path2d = new Path2D();
  path2d.moveTo(points[0][0], points[0][1]);
  bezierPath2d(path2d, xyz(points[0]), xyz(points[1]), xyz(points[2]), xyz(points[3]));
  bezierPath2d(path2d, xyz(points[3]), xyz(points[9]), xyz(points[11]), xyz(points[7]));
  bezierPath2d(path2d, xyz(points[7]), xyz(points[6]), xyz(points[5]), xyz(points[4]));
  bezierPath2d(path2d, xyz(points[4]), xyz(points[10]), xyz(points[8]), xyz(points[0]));
  return path2d;
}
function xyz(arr) {return {"x": arr[0], "y": arr[1], "z": 0}};
function createPath2d(points) {
  const path2d = new Path2D();
  path2d.moveTo(points[0][0], points[0][1]);
  path2d.bezierCurveTo(points[1][0], points[1][1], points[2][0], points[2][1], points[3][0], points[3][1]);
  path2d.bezierCurveTo(points[9][0], points[9][1], points[11][0], points[11][1], points[7][0], points[7][1]);
  path2d.bezierCurveTo(points[6][0], points[6][1], points[5][0], points[5][1], points[4][0], points[4][1]);
  path2d.bezierCurveTo(points[10][0], points[10][1], points[8][0], points[8][1], points[0][0], points[0][1]);
  return path2d;
}
function createPath(points) {
  let d = "";
  const polygon = document.createElementNS("http://www.w3.org/2000/svg", "path");
  d += `M ${points[0][0]} ${points[0][1]} `;
  d += `C ${points[1][0]} ${points[1][1]}, ${points[2][0]} ${points[2][1]}, ${points[3][0]} ${points[3][1]} `;
  d += `C ${points[9][0]} ${points[9][1]}, ${points[11][0]} ${points[11][1]}, ${points[7][0]} ${points[7][1]} `;
  d += `C ${points[6][0]} ${points[6][1]}, ${points[5][0]} ${points[5][1]}, ${points[4][0]} ${points[4][1]} `;
  d += `C ${points[10][0]} ${points[10][1]}, ${points[8][0]} ${points[8][1]}, ${points[0][0]} ${points[0][1]} `;
  polygon.setAttribute("d", d);
  polygon.setAttribute("fill", "black");
  return polygon;
}
function bezierPath2d(path2d, p0, p1, p2, p3) {
  for (let i = 0; i < 1; i += 0.001) {
    const p = bezier(i, p0, p1, p2, p3);
    path2d.lineTo(p.x, p.y);
  }
}
function bezier(t, p0, p1, p2, p3) {
  const a = lerp(t, p0, p1);
  const b = lerp(t, p1, p2);
  const c = lerp(t, p2, p3);
  const d = lerp(t, a, b);
  const e = lerp(t, b, c);
  const f = lerp(t, d, e);
  return f;
}
function lerp(t, a, b) {
   const dx = (b.x - a.x);
   const dy = (b.y - a.y);
   const dz = (b.z - a.z);
   return {
    "x": a.x + t * dx,
    "y": a.y + t * dy,
    "z": a.z + t * dz,
   }
}