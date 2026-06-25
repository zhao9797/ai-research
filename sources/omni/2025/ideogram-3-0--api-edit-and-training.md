
==================== https://developer.ideogram.ai/api-reference/api-reference/inpaint-v3.md ====================
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Inpaint with Ideogram 3.0

POST https://api.ideogram.ai/v1/ideogram-v3/inpaint
Content-Type: multipart/form-data

Inpaint a given image synchronously using the provided mask with Ideogram 3.0. The mask indicates which part of the image
should be edited, while the prompt and chosen style can further guide the edit.

Supported image formats include JPEG, PNG, and WebP.

Images links are available for a limited period of time; if you would like to keep the image, you must download it.

Reference: https://developer.ideogram.ai/api-reference/api-reference/inpaint-v3

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /v1/ideogram-v3/inpaint:
    post:
      operationId: post-inpaint-image-v-3
      summary: Inpaint with Ideogram 3.0
      description: >
        Inpaint a given image synchronously using the provided mask with
        Ideogram 3.0. The mask indicates which part of the image

        should be edited, while the prompt and chosen style can further guide
        the edit.

        Supported image formats include JPEG, PNG, and WebP.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      tags:
        - subpackage_generate
      parameters:
        - name: Api-Key
          in: header
          description: >-
            API key for access control. Use in the header with the name
            \"Api-Key\"
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Image edits generated successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ImageGenerationResponseV3'
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                description: Any type
        '401':
          description: Not authorized to generate an image.
          content:
            application/json:
              schema:
                description: Any type
        '422':
          description: Prompt or Initial Image failed the safety checks.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GenerateImageSafetyError'
        '429':
          description: Too many requests.
          content:
            application/json:
              schema:
                description: Any type
      requestBody:
        description: A request to inpaint an image with Ideogram 3.0.
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                image:
                  type: string
                  format: binary
                  description: >-
                    The image being edited (max size 10MB); only JPEG, WebP and
                    PNG formats are supported at this time.
                mask:
                  type: string
                  format: binary
                  description: >-
                    A black and white image of the same size as the image being
                    edited (max size 10MB). Black regions in the mask should
                    match up with the regions of the image that you would like
                    to edit; only JPEG, WebP and PNG formats are supported at
                    this time.
                prompt:
                  type: string
                  description: The prompt used to describe the edited result.
                magic_prompt:
                  $ref: '#/components/schemas/MagicPromptOption'
                num_images:
                  $ref: '#/components/schemas/NumImages'
                seed:
                  $ref: '#/components/schemas/Seed'
                rendering_speed:
                  $ref: '#/components/schemas/RenderingSpeed'
                style_type:
                  $ref: '#/components/schemas/StyleTypeV3'
                style_preset:
                  $ref: '#/components/schemas/StylePresetV3'
                color_palette:
                  $ref: '#/components/schemas/ColorPaletteWithPresetNameOrMembers'
                style_codes:
                  $ref: '#/components/schemas/StyleCodes'
                style_reference_images:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    A set of images to use as style references (maximum total
                    size 10MB across all style references). The images should be
                    in JPEG, PNG or WebP format.
                character_reference_images:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    Generations with character reference are subject to the
                    character reference pricing. A set of images to use as
                    character references (maximum total size 10MB across all
                    character references), currently only supports 1 character
                    reference image. The images should be in JPEG, PNG or WebP
                    format.
                character_reference_images_mask:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    Optional masks for character reference images. When
                    provided, must match the number of
                    character_reference_images. Each mask should be a grayscale
                    image of the same dimensions as the corresponding character
                    reference image. The images should be in JPEG, PNG or WebP
                    format.
              required:
                - image
                - mask
                - prompt
servers:
  - url: https://api.ideogram.ai
    description: https://api.ideogram.ai
components:
  schemas:
    MagicPromptOption:
      type: string
      enum:
        - AUTO
        - 'ON'
        - 'OFF'
      description: >-
        Determine if MagicPrompt should be used in generating the request or
        not.
      title: MagicPromptOption
    NumImages:
      type: integer
      default: 1
      description: The number of images to generate.
      title: NumImages
    Seed:
      type: integer
      description: Random seed. Set for reproducible generation.
      title: Seed
    RenderingSpeed:
      type: string
      enum:
        - FLASH
        - TURBO
        - DEFAULT
        - QUALITY
      default: DEFAULT
      description: The rendering speed to use.
      title: RenderingSpeed
    StyleTypeV3:
      type: string
      enum:
        - AUTO
        - GENERAL
        - REALISTIC
        - DESIGN
        - FICTION
      default: GENERAL
      description: The style type to generate with.
      title: StyleTypeV3
    StylePresetV3:
      type: string
      enum:
        - 80S_ILLUSTRATION
        - 90S_NOSTALGIA
        - ABSTRACT_ORGANIC
        - ANALOG_NOSTALGIA
        - ART_BRUT
        - ART_DECO
        - ART_POSTER
        - AURA
        - AVANT_GARDE
        - BAUHAUS
        - BLUEPRINT
        - BLURRY_MOTION
        - BRIGHT_ART
        - C4D_CARTOON
        - CHILDRENS_BOOK
        - COLLAGE
        - COLORING_BOOK_I
        - COLORING_BOOK_II
        - CUBISM
        - DARK_AURA
        - DOODLE
        - DOUBLE_EXPOSURE
        - DRAMATIC_CINEMA
        - EDITORIAL
        - EMOTIONAL_MINIMAL
        - ETHEREAL_PARTY
        - EXPIRED_FILM
        - FLAT_ART
        - FLAT_VECTOR
        - FOREST_REVERIE
        - GEO_MINIMALIST
        - GLASS_PRISM
        - GOLDEN_HOUR
        - GRAFFITI_I
        - GRAFFITI_II
        - HALFTONE_PRINT
        - HIGH_CONTRAST
        - HIPPIE_ERA
        - ICONIC
        - JAPANDI_FUSION
        - JAZZY
        - LONG_EXPOSURE
        - MAGAZINE_EDITORIAL
        - MINIMAL_ILLUSTRATION
        - MIXED_MEDIA
        - MONOCHROME
        - NIGHTLIFE
        - OIL_PAINTING
        - OLD_CARTOONS
        - PAINT_GESTURE
        - POP_ART
        - RETRO_ETCHING
        - RIVIERA_POP
        - SPOTLIGHT_80S
        - STYLIZED_RED
        - SURREAL_COLLAGE
        - TRAVEL_POSTER
        - VINTAGE_GEO
        - VINTAGE_POSTER
        - WATERCOLOR
        - WEIRD
        - WOODBLOCK_PRINT
      description: >-
        A predefined style preset that applies a specific artistic style to the
        generated image.
      title: StylePresetV3
    ColorPalettePresetName:
      type: string
      enum:
        - EMBER
        - FRESH
        - JUNGLE
        - MAGIC
        - MELON
        - MOSAIC
        - PASTEL
        - ULTRAMARINE
      description: A color palette preset value.
      title: ColorPalettePresetName
    ColorPaletteWithPresetName:
      type: object
      properties:
        name:
          $ref: '#/components/schemas/ColorPalettePresetName'
      required:
        - name
      title: ColorPaletteWithPresetName
    ColorPaletteMember:
      type: object
      properties:
        color_hex:
          type: string
          description: >-
            The hexadecimal representation of the color with an optional chosen
            weight.
        color_weight:
          type: number
          format: double
          description: The weight of the color in the color palette.
      required:
        - color_hex
      description: A member of a color palette.
      title: ColorPaletteMember
    ColorPaletteWithMembers:
      type: object
      properties:
        members:
          type: array
          items:
            $ref: '#/components/schemas/ColorPaletteMember'
          description: >
            A list of ColorPaletteMembers that define the color palette. Each
            color palette member

            consists of a required color hex and an optional weight between 0.05
            and 1.0 (inclusive).

            It is recommended that these weights descend from highest to lowest
            for the color hexes provided.
      required:
        - members
      description: >-
        A color palette represented only via its members. Cannot be used in
        conjunction with preset name.
      title: ColorPaletteWithMembers
    ColorPaletteWithPresetNameOrMembers:
      oneOf:
        - $ref: '#/components/schemas/ColorPaletteWithPresetName'
        - $ref: '#/components/schemas/ColorPaletteWithMembers'
      description: >-
        A color palette for generation, must EITHER be specified via one of the
        presets (name) or explicitly via hexadecimal representations of the
        color with optional weights (members). Not supported by V_1, V_1_TURBO,
        V_2A and V_2A_TURBO models.
      title: ColorPaletteWithPresetNameOrMembers
    StyleCode:
      type: string
      description: The 8 character hexadecimal representation of the style code.
      title: StyleCode
    StyleCodes:
      type: array
      items:
        $ref: '#/components/schemas/StyleCode'
      description: >-
        A list of 8 character hexadecimal codes representing the style of the
        image. Cannot be used in conjunction with style_reference_images or
        style_type.
      title: StyleCodes
    ResolutionV3:
      type: string
      enum:
        - 512x1536
        - 576x1408
        - 576x1472
        - 576x1536
        - 640x1344
        - 640x1408
        - 640x1472
        - 640x1536
        - 704x1152
        - 704x1216
        - 704x1280
        - 704x1344
        - 704x1408
        - 704x1472
        - 736x1312
        - 768x1088
        - 768x1216
        - 768x1280
        - 768x1344
        - 800x1280
        - 832x960
        - 832x1024
        - 832x1088
        - 832x1152
        - 832x1216
        - 832x1248
        - 864x1152
        - 896x960
        - 896x1024
        - 896x1088
        - 896x1120
        - 896x1152
        - 960x832
        - 960x896
        - 960x1024
        - 960x1088
        - 1024x832
        - 1024x896
        - 1024x960
        - 1024x1024
        - 1088x768
        - 1088x832
        - 1088x896
        - 1088x960
        - 1120x896
        - 1152x704
        - 1152x832
        - 1152x864
        - 1152x896
        - 1216x704
        - 1216x768
        - 1216x832
        - 1248x832
        - 1280x704
        - 1280x768
        - 1280x800
        - 1312x736
        - 1344x640
        - 1344x704
        - 1344x768
        - 1408x576
        - 1408x640
        - 1408x704
        - 1472x576
        - 1472x640
        - 1472x704
        - 1536x512
        - 1536x576
        - 1536x640
      description: The resolutions supported for Ideogram 3.0.
      title: ResolutionV3
    ImageGenerationObjectV3:
      type: object
      properties:
        url:
          type:
            - string
            - 'null'
          format: uri
          description: The direct link to the image generated.
        prompt:
          type: string
          description: >-
            The prompt used for the generation. This may be different from the
            original prompt.
        resolution:
          $ref: '#/components/schemas/ResolutionV3'
        upscaled_resolution:
          type: string
          description: >-
            Output resolution, only used if operations alters image dimensions,
            such as upscale, crop etc.
        is_image_safe:
          type: boolean
          description: >-
            Whether this request passes safety checks. If false, the url field
            will be empty.
        seed:
          type: integer
          description: Random seed. Set for reproducible generation.
        style_type:
          $ref: '#/components/schemas/StyleTypeV3'
      required:
        - prompt
        - resolution
        - is_image_safe
        - seed
      title: ImageGenerationObjectV3
    ImageGenerationResponseV3:
      type: object
      properties:
        created:
          type: string
          format: date-time
          description: The time the request was created.
        data:
          type: array
          items:
            $ref: '#/components/schemas/ImageGenerationObjectV3'
          description: A list of ImageObjects that contain the generated image(s).
      required:
        - created
        - data
      description: >-
        The response which contains information about the generated image,
        including the download link.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      title: ImageGenerationResponseV3
    GenerateImageSafetyError:
      type: object
      properties:
        error:
          type: string
      required:
        - error
      title: GenerateImageSafetyError
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Api-Key
      description: API key for access control. Use in the header with the name \"Api-Key\"

```

## Examples

**Request**

```json
{
  "image": "<file: <file1>>",
  "mask": "<file: <file1>>",
  "prompt": "A photo of a cat wearing a hat.",
  "style_type": "AUTO",
  "style_reference_images": [],
  "character_reference_images": [],
  "character_reference_images_mask": []
}
```

**Response**

```json
{
  "created": "2000-01-23 04:56:07+00:00",
  "data": [
    {
      "prompt": "A photo of a cat wearing a hat.",
      "resolution": "1024x1024",
      "is_image_safe": true,
      "seed": 12345,
      "url": "https://ideogram.ai/api/images/ephemeral/xtdZiqPwRxqY1Y7NExFmzB.png?exp=1743867804&sig=e13e12677633f646d8531a153d20e2d3698dca9ee7661ee5ba4f3b64e7ec3f89",
      "style_type": "AUTO"
    }
  ]
}
```

**SDK Code**

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/inpaint",
  headers={
    "Api-Key": "<apiKey>"
  },
  data={
    "prompt": "A photo of a cat wearing a hat.",
    "rendering_speed": "DEFAULT"
  },
  files={
    "image": open("<file1>", "rb"),
    "mask": open("<file1>", "rb"),
  }
)
print(response.json())
with open('output.png', 'wb') as f:
  f.write(requests.get(response.json()['data'][0]['url']).content)

```

```typescript
const formData = new FormData();
formData.append('prompt', 'A photo of a cat');
formData.append('rendering_speed', 'TURBO');
const response = await fetch('https://api.ideogram.ai/v1/ideogram-v3/inpaint', {
  method: 'POST',
  headers: { 'Api-Key': '<apiKey>' },
  body: formData
});
const data = await response.json();
console.log(data);

```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://api.ideogram.ai/v1/ideogram-v3/inpaint"

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Api-Key", "<apiKey>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("https://api.ideogram.ai/v1/ideogram-v3/inpaint")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Api-Key"] = '<apiKey>'

response = http.request(request)
puts response.read_body
```

```java
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;

HttpResponse<String> response = Unirest.post("https://api.ideogram.ai/v1/ideogram-v3/inpaint")
  .header("Api-Key", "<apiKey>")
  .asString();
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'https://api.ideogram.ai/v1/ideogram-v3/inpaint', [
  'multipart' => [
    [
        'name' => 'image',
        'filename' => '<file1>',
        'contents' => null
    ],
    [
        'name' => 'mask',
        'filename' => '<file1>',
        'contents' => null
    ],
    [
        'name' => 'prompt',
        'contents' => 'A photo of a cat wearing a hat.'
    ],
    [
        'name' => 'style_type',
        'contents' => 'AUTO'
    ]
  ]
  'headers' => [
    'Api-Key' => '<apiKey>',
  ],
]);

echo $response->getBody();
```

```csharp
using RestSharp;

var client = new RestClient("https://api.ideogram.ai/v1/ideogram-v3/inpaint");
var request = new RestRequest(Method.POST);
request.AddHeader("Api-Key", "<apiKey>");
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = [
  "Api-Key": "<apiKey>",
]
let parameters = [
  [
    "name": "image",
    "fileName": "<file1>"
  ],
  [
    "name": "mask",
    "fileName": "<file1>"
  ],
  [
    "name": "prompt",
    "value": "A photo of a cat wearing a hat."
  ],
  [
    "name": "magic_prompt",
    "value": 
  ],
  [
    "name": "num_images",
    "value": 
  ],
  [
    "name": "seed",
    "value": 
  ],
  [
    "name": "rendering_speed",
    "value": 
  ],
  [
    "name": "style_type",
    "value": "AUTO"
  ],
  [
    "name": "style_preset",
    "value": 
  ],
  [
    "name": "color_palette",
    "value": 
  ],
  [
    "name": "style_codes",
    "value": 
  ]
]

var body = ""
var error: NSError? = nil
for param in parameters {
  let paramName = param["name"]!
  body += "--\(boundary)\r\n"
  body += "Content-Disposition:form-data; name=\"\(paramName)\""
  if let filename = param["fileName"] {
    let contentType = param["content-type"]!
    let fileContent = String(contentsOfFile: filename, encoding: String.Encoding.utf8)
    if (error != nil) {
      print(error as Any)
    }
    body += "; filename=\"\(filename)\"\r\n"
    body += "Content-Type: \(contentType)\r\n\r\n"
    body += fileContent
  } else if let paramValue = param["value"] {
    body += "\r\n\r\n\(paramValue)"
  }
}

let request = NSMutableURLRequest(url: NSURL(string: "https://api.ideogram.ai/v1/ideogram-v3/inpaint")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "POST"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```
==================== https://developer.ideogram.ai/api-reference/api-reference/replace-background-v3.md ====================
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Replace Background with Ideogram 3.0

POST https://api.ideogram.ai/v1/ideogram-v3/replace-background
Content-Type: multipart/form-data

Replace the background of a given image synchronously using a prompt with Ideogram 3.0. The foreground subject
will be identified and kept, while the background is replaced based on the prompt and chosen style.
Supported image formats include JPEG, PNG, and WebP.
Images links are available for a limited period of time; if you would like to keep the image, you must download it.

Reference: https://developer.ideogram.ai/api-reference/api-reference/replace-background-v3

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /v1/ideogram-v3/replace-background:
    post:
      operationId: post-replace-background-v-3
      summary: Replace Background with Ideogram 3.0
      description: >
        Replace the background of a given image synchronously using a prompt
        with Ideogram 3.0. The foreground subject

        will be identified and kept, while the background is replaced based on
        the prompt and chosen style.

        Supported image formats include JPEG, PNG, and WebP.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      tags:
        - subpackage_generate
      parameters:
        - name: Api-Key
          in: header
          description: >-
            API key for access control. Use in the header with the name
            \"Api-Key\"
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Background replacement generated successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ImageGenerationResponseV3'
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                description: Any type
        '401':
          description: Not authorized to generate an image.
          content:
            application/json:
              schema:
                description: Any type
        '422':
          description: Prompt or Initial Image failed the safety checks.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GenerateImageSafetyError'
        '429':
          description: Too many requests.
          content:
            application/json:
              schema:
                description: Any type
      requestBody:
        description: A request to replace the background of an image with Ideogram 3.0.
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                image:
                  type: string
                  format: binary
                  description: >-
                    The image whose background is being replaced (max size
                    10MB); only JPEG, WebP and PNG formats are supported at this
                    time.
                prompt:
                  type: string
                  description: The prompt describing the desired new background.
                magic_prompt:
                  $ref: '#/components/schemas/MagicPromptOption'
                num_images:
                  $ref: '#/components/schemas/NumImages'
                seed:
                  $ref: '#/components/schemas/Seed'
                rendering_speed:
                  $ref: '#/components/schemas/RenderingSpeed'
                style_preset:
                  $ref: '#/components/schemas/StylePresetV3'
                color_palette:
                  $ref: '#/components/schemas/ColorPaletteWithPresetNameOrMembers'
                style_codes:
                  $ref: '#/components/schemas/StyleCodes'
                style_reference_images:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    A set of images to use as style references (maximum total
                    size 10MB across all style references). The images should be
                    in JPEG, PNG or WebP format.
              required:
                - image
                - prompt
servers:
  - url: https://api.ideogram.ai
    description: https://api.ideogram.ai
components:
  schemas:
    MagicPromptOption:
      type: string
      enum:
        - AUTO
        - 'ON'
        - 'OFF'
      description: >-
        Determine if MagicPrompt should be used in generating the request or
        not.
      title: MagicPromptOption
    NumImages:
      type: integer
      default: 1
      description: The number of images to generate.
      title: NumImages
    Seed:
      type: integer
      description: Random seed. Set for reproducible generation.
      title: Seed
    RenderingSpeed:
      type: string
      enum:
        - FLASH
        - TURBO
        - DEFAULT
        - QUALITY
      default: DEFAULT
      description: The rendering speed to use.
      title: RenderingSpeed
    StylePresetV3:
      type: string
      enum:
        - 80S_ILLUSTRATION
        - 90S_NOSTALGIA
        - ABSTRACT_ORGANIC
        - ANALOG_NOSTALGIA
        - ART_BRUT
        - ART_DECO
        - ART_POSTER
        - AURA
        - AVANT_GARDE
        - BAUHAUS
        - BLUEPRINT
        - BLURRY_MOTION
        - BRIGHT_ART
        - C4D_CARTOON
        - CHILDRENS_BOOK
        - COLLAGE
        - COLORING_BOOK_I
        - COLORING_BOOK_II
        - CUBISM
        - DARK_AURA
        - DOODLE
        - DOUBLE_EXPOSURE
        - DRAMATIC_CINEMA
        - EDITORIAL
        - EMOTIONAL_MINIMAL
        - ETHEREAL_PARTY
        - EXPIRED_FILM
        - FLAT_ART
        - FLAT_VECTOR
        - FOREST_REVERIE
        - GEO_MINIMALIST
        - GLASS_PRISM
        - GOLDEN_HOUR
        - GRAFFITI_I
        - GRAFFITI_II
        - HALFTONE_PRINT
        - HIGH_CONTRAST
        - HIPPIE_ERA
        - ICONIC
        - JAPANDI_FUSION
        - JAZZY
        - LONG_EXPOSURE
        - MAGAZINE_EDITORIAL
        - MINIMAL_ILLUSTRATION
        - MIXED_MEDIA
        - MONOCHROME
        - NIGHTLIFE
        - OIL_PAINTING
        - OLD_CARTOONS
        - PAINT_GESTURE
        - POP_ART
        - RETRO_ETCHING
        - RIVIERA_POP
        - SPOTLIGHT_80S
        - STYLIZED_RED
        - SURREAL_COLLAGE
        - TRAVEL_POSTER
        - VINTAGE_GEO
        - VINTAGE_POSTER
        - WATERCOLOR
        - WEIRD
        - WOODBLOCK_PRINT
      description: >-
        A predefined style preset that applies a specific artistic style to the
        generated image.
      title: StylePresetV3
    ColorPalettePresetName:
      type: string
      enum:
        - EMBER
        - FRESH
        - JUNGLE
        - MAGIC
        - MELON
        - MOSAIC
        - PASTEL
        - ULTRAMARINE
      description: A color palette preset value.
      title: ColorPalettePresetName
    ColorPaletteWithPresetName:
      type: object
      properties:
        name:
          $ref: '#/components/schemas/ColorPalettePresetName'
      required:
        - name
      title: ColorPaletteWithPresetName
    ColorPaletteMember:
      type: object
      properties:
        color_hex:
          type: string
          description: >-
            The hexadecimal representation of the color with an optional chosen
            weight.
        color_weight:
          type: number
          format: double
          description: The weight of the color in the color palette.
      required:
        - color_hex
      description: A member of a color palette.
      title: ColorPaletteMember
    ColorPaletteWithMembers:
      type: object
      properties:
        members:
          type: array
          items:
            $ref: '#/components/schemas/ColorPaletteMember'
          description: >
            A list of ColorPaletteMembers that define the color palette. Each
            color palette member

            consists of a required color hex and an optional weight between 0.05
            and 1.0 (inclusive).

            It is recommended that these weights descend from highest to lowest
            for the color hexes provided.
      required:
        - members
      description: >-
        A color palette represented only via its members. Cannot be used in
        conjunction with preset name.
      title: ColorPaletteWithMembers
    ColorPaletteWithPresetNameOrMembers:
      oneOf:
        - $ref: '#/components/schemas/ColorPaletteWithPresetName'
        - $ref: '#/components/schemas/ColorPaletteWithMembers'
      description: >-
        A color palette for generation, must EITHER be specified via one of the
        presets (name) or explicitly via hexadecimal representations of the
        color with optional weights (members). Not supported by V_1, V_1_TURBO,
        V_2A and V_2A_TURBO models.
      title: ColorPaletteWithPresetNameOrMembers
    StyleCode:
      type: string
      description: The 8 character hexadecimal representation of the style code.
      title: StyleCode
    StyleCodes:
      type: array
      items:
        $ref: '#/components/schemas/StyleCode'
      description: >-
        A list of 8 character hexadecimal codes representing the style of the
        image. Cannot be used in conjunction with style_reference_images or
        style_type.
      title: StyleCodes
    ResolutionV3:
      type: string
      enum:
        - 512x1536
        - 576x1408
        - 576x1472
        - 576x1536
        - 640x1344
        - 640x1408
        - 640x1472
        - 640x1536
        - 704x1152
        - 704x1216
        - 704x1280
        - 704x1344
        - 704x1408
        - 704x1472
        - 736x1312
        - 768x1088
        - 768x1216
        - 768x1280
        - 768x1344
        - 800x1280
        - 832x960
        - 832x1024
        - 832x1088
        - 832x1152
        - 832x1216
        - 832x1248
        - 864x1152
        - 896x960
        - 896x1024
        - 896x1088
        - 896x1120
        - 896x1152
        - 960x832
        - 960x896
        - 960x1024
        - 960x1088
        - 1024x832
        - 1024x896
        - 1024x960
        - 1024x1024
        - 1088x768
        - 1088x832
        - 1088x896
        - 1088x960
        - 1120x896
        - 1152x704
        - 1152x832
        - 1152x864
        - 1152x896
        - 1216x704
        - 1216x768
        - 1216x832
        - 1248x832
        - 1280x704
        - 1280x768
        - 1280x800
        - 1312x736
        - 1344x640
        - 1344x704
        - 1344x768
        - 1408x576
        - 1408x640
        - 1408x704
        - 1472x576
        - 1472x640
        - 1472x704
        - 1536x512
        - 1536x576
        - 1536x640
      description: The resolutions supported for Ideogram 3.0.
      title: ResolutionV3
    StyleTypeV3:
      type: string
      enum:
        - AUTO
        - GENERAL
        - REALISTIC
        - DESIGN
        - FICTION
      default: GENERAL
      description: The style type to generate with.
      title: StyleTypeV3
    ImageGenerationObjectV3:
      type: object
      properties:
        url:
          type:
            - string
            - 'null'
          format: uri
          description: The direct link to the image generated.
        prompt:
          type: string
          description: >-
            The prompt used for the generation. This may be different from the
            original prompt.
        resolution:
          $ref: '#/components/schemas/ResolutionV3'
        upscaled_resolution:
          type: string
          description: >-
            Output resolution, only used if operations alters image dimensions,
            such as upscale, crop etc.
        is_image_safe:
          type: boolean
          description: >-
            Whether this request passes safety checks. If false, the url field
            will be empty.
        seed:
          type: integer
          description: Random seed. Set for reproducible generation.
        style_type:
          $ref: '#/components/schemas/StyleTypeV3'
      required:
        - prompt
        - resolution
        - is_image_safe
        - seed
      title: ImageGenerationObjectV3
    ImageGenerationResponseV3:
      type: object
      properties:
        created:
          type: string
          format: date-time
          description: The time the request was created.
        data:
          type: array
          items:
            $ref: '#/components/schemas/ImageGenerationObjectV3'
          description: A list of ImageObjects that contain the generated image(s).
      required:
        - created
        - data
      description: >-
        The response which contains information about the generated image,
        including the download link.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      title: ImageGenerationResponseV3
    GenerateImageSafetyError:
      type: object
      properties:
        error:
          type: string
      required:
        - error
      title: GenerateImageSafetyError
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Api-Key
      description: API key for access control. Use in the header with the name \"Api-Key\"

```

## Examples

**Request**

```json
{
  "image": "<file: <file1>>",
  "prompt": "Add a forest in the background",
  "magic_prompt": "ON",
  "rendering_speed": "QUALITY",
  "style_reference_images": []
}
```

**Response**

```json
{
  "created": "2000-01-23 04:56:07+00:00",
  "data": [
    {
      "prompt": "Add a forest in the background",
      "resolution": "1280x800",
      "is_image_safe": true,
      "seed": 12345,
      "url": "https://ideogram.ai/api/images/ephemeral/xtdZiqPwRxqY1Y7NExFmzB.png?exp=1743867804&sig=e13e12677633f646d8531a153d20e2d3698dca9ee7661ee5ba4f3b64e7ec3f89",
      "style_type": "GENERAL"
    }
  ]
}
```

**SDK Code**

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/replace-background",
  headers={
    "Api-Key": "<apiKey>" 
  },
  data={
    "prompt": "Add a forest in the background",
    "magic_prompt": "ON"
  },
  files={
    "image": open("<file1>", "rb"),
  }
)
print(response.json())
with open('output.png', 'wb') as f:
  f.write(requests.get(response.json()['data'][0]['url']).content)

```

```typescript
const formData = new FormData();
formData.append('prompt', 'Add a forest in the background');
formData.append('image', '<file1>');
const response = await fetch('https://api.ideogram.ai/v1/ideogram-v3/replace-background', {
  method: 'POST',
  headers: { 'Api-Key': '<apiKey>' },
  body: formData
});
const data = await response.json();
console.log(data);

```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://api.ideogram.ai/v1/ideogram-v3/replace-background"

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Api-Key", "<apiKey>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("https://api.ideogram.ai/v1/ideogram-v3/replace-background")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Api-Key"] = '<apiKey>'

response = http.request(request)
puts response.read_body
```

```java
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;

HttpResponse<String> response = Unirest.post("https://api.ideogram.ai/v1/ideogram-v3/replace-background")
  .header("Api-Key", "<apiKey>")
  .asString();
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'https://api.ideogram.ai/v1/ideogram-v3/replace-background', [
  'multipart' => [
    [
        'name' => 'image',
        'filename' => '<file1>',
        'contents' => null
    ],
    [
        'name' => 'prompt',
        'contents' => 'Add a forest in the background'
    ],
    [
        'name' => 'magic_prompt',
        'contents' => 'ON'
    ],
    [
        'name' => 'rendering_speed',
        'contents' => 'QUALITY'
    ]
  ]
  'headers' => [
    'Api-Key' => '<apiKey>',
  ],
]);

echo $response->getBody();
```

```csharp
using RestSharp;

var client = new RestClient("https://api.ideogram.ai/v1/ideogram-v3/replace-background");
var request = new RestRequest(Method.POST);
request.AddHeader("Api-Key", "<apiKey>");
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = [
  "Api-Key": "<apiKey>",
]
let parameters = [
  [
    "name": "image",
    "fileName": "<file1>"
  ],
  [
    "name": "prompt",
    "value": "Add a forest in the background"
  ],
  [
    "name": "magic_prompt",
    "value": "ON"
  ],
  [
    "name": "num_images",
    "value": 
  ],
  [
    "name": "seed",
    "value": 
  ],
  [
    "name": "rendering_speed",
    "value": "QUALITY"
  ],
  [
    "name": "style_preset",
    "value": 
  ],
  [
    "name": "color_palette",
    "value": 
  ],
  [
    "name": "style_codes",
    "value": 
  ]
]

var body = ""
var error: NSError? = nil
for param in parameters {
  let paramName = param["name"]!
  body += "--\(boundary)\r\n"
  body += "Content-Disposition:form-data; name=\"\(paramName)\""
  if let filename = param["fileName"] {
    let contentType = param["content-type"]!
    let fileContent = String(contentsOfFile: filename, encoding: String.Encoding.utf8)
    if (error != nil) {
      print(error as Any)
    }
    body += "; filename=\"\(filename)\"\r\n"
    body += "Content-Type: \(contentType)\r\n\r\n"
    body += fileContent
  } else if let paramValue = param["value"] {
    body += "\r\n\r\n\(paramValue)"
  }
}

let request = NSMutableURLRequest(url: NSURL(string: "https://api.ideogram.ai/v1/ideogram-v3/replace-background")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "POST"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```
==================== https://developer.ideogram.ai/api-reference/api-reference/reframe-v3.md ====================
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Reframe with Ideogram 3.0

POST https://api.ideogram.ai/v1/ideogram-v3/reframe
Content-Type: multipart/form-data

Reframe a square image to a chosen resolution with Ideogram 3.0. The supported image formats include JPEG, PNG, and WebP.

Image links are available for a limited period of time; if you would like to keep the image, you must download it.

Reference: https://developer.ideogram.ai/api-reference/api-reference/reframe-v3

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /v1/ideogram-v3/reframe:
    post:
      operationId: post-reframe-image-v-3
      summary: Reframe with Ideogram 3.0
      description: >
        Reframe a square image to a chosen resolution with Ideogram 3.0. The
        supported image formats include JPEG, PNG, and WebP.

        Image links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      tags:
        - subpackage_generate
      parameters:
        - name: Api-Key
          in: header
          description: >-
            API key for access control. Use in the header with the name
            \"Api-Key\"
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Image re-frames generated successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ImageGenerationResponseV3'
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                description: Any type
        '401':
          description: Not authorized to generate an image.
          content:
            application/json:
              schema:
                description: Any type
        '422':
          description: Prompt or Image failed the safety checks.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GenerateImageSafetyError'
        '429':
          description: Too many requests.
          content:
            application/json:
              schema:
                description: Any type
      requestBody:
        description: A request to reframe an image in a new resolution.
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                image:
                  type: string
                  format: binary
                  description: >-
                    The image being reframed (max size 10MB); only JPEG, WebP
                    and PNG formats are supported at this time.
                resolution:
                  $ref: '#/components/schemas/ResolutionV3'
                num_images:
                  $ref: '#/components/schemas/NumImages'
                seed:
                  $ref: '#/components/schemas/Seed'
                rendering_speed:
                  $ref: '#/components/schemas/RenderingSpeed'
                style_preset:
                  $ref: '#/components/schemas/StylePresetV3'
                color_palette:
                  $ref: '#/components/schemas/ColorPaletteWithPresetNameOrMembers'
                style_codes:
                  $ref: '#/components/schemas/StyleCodes'
                style_reference_images:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    A set of images to use as style references (maximum total
                    size 10MB across all style references). The images should be
                    in JPEG, PNG or WebP format.
              required:
                - image
                - resolution
servers:
  - url: https://api.ideogram.ai
    description: https://api.ideogram.ai
components:
  schemas:
    ResolutionV3:
      type: string
      enum:
        - 512x1536
        - 576x1408
        - 576x1472
        - 576x1536
        - 640x1344
        - 640x1408
        - 640x1472
        - 640x1536
        - 704x1152
        - 704x1216
        - 704x1280
        - 704x1344
        - 704x1408
        - 704x1472
        - 736x1312
        - 768x1088
        - 768x1216
        - 768x1280
        - 768x1344
        - 800x1280
        - 832x960
        - 832x1024
        - 832x1088
        - 832x1152
        - 832x1216
        - 832x1248
        - 864x1152
        - 896x960
        - 896x1024
        - 896x1088
        - 896x1120
        - 896x1152
        - 960x832
        - 960x896
        - 960x1024
        - 960x1088
        - 1024x832
        - 1024x896
        - 1024x960
        - 1024x1024
        - 1088x768
        - 1088x832
        - 1088x896
        - 1088x960
        - 1120x896
        - 1152x704
        - 1152x832
        - 1152x864
        - 1152x896
        - 1216x704
        - 1216x768
        - 1216x832
        - 1248x832
        - 1280x704
        - 1280x768
        - 1280x800
        - 1312x736
        - 1344x640
        - 1344x704
        - 1344x768
        - 1408x576
        - 1408x640
        - 1408x704
        - 1472x576
        - 1472x640
        - 1472x704
        - 1536x512
        - 1536x576
        - 1536x640
      description: The resolutions supported for Ideogram 3.0.
      title: ResolutionV3
    NumImages:
      type: integer
      default: 1
      description: The number of images to generate.
      title: NumImages
    Seed:
      type: integer
      description: Random seed. Set for reproducible generation.
      title: Seed
    RenderingSpeed:
      type: string
      enum:
        - FLASH
        - TURBO
        - DEFAULT
        - QUALITY
      default: DEFAULT
      description: The rendering speed to use.
      title: RenderingSpeed
    StylePresetV3:
      type: string
      enum:
        - 80S_ILLUSTRATION
        - 90S_NOSTALGIA
        - ABSTRACT_ORGANIC
        - ANALOG_NOSTALGIA
        - ART_BRUT
        - ART_DECO
        - ART_POSTER
        - AURA
        - AVANT_GARDE
        - BAUHAUS
        - BLUEPRINT
        - BLURRY_MOTION
        - BRIGHT_ART
        - C4D_CARTOON
        - CHILDRENS_BOOK
        - COLLAGE
        - COLORING_BOOK_I
        - COLORING_BOOK_II
        - CUBISM
        - DARK_AURA
        - DOODLE
        - DOUBLE_EXPOSURE
        - DRAMATIC_CINEMA
        - EDITORIAL
        - EMOTIONAL_MINIMAL
        - ETHEREAL_PARTY
        - EXPIRED_FILM
        - FLAT_ART
        - FLAT_VECTOR
        - FOREST_REVERIE
        - GEO_MINIMALIST
        - GLASS_PRISM
        - GOLDEN_HOUR
        - GRAFFITI_I
        - GRAFFITI_II
        - HALFTONE_PRINT
        - HIGH_CONTRAST
        - HIPPIE_ERA
        - ICONIC
        - JAPANDI_FUSION
        - JAZZY
        - LONG_EXPOSURE
        - MAGAZINE_EDITORIAL
        - MINIMAL_ILLUSTRATION
        - MIXED_MEDIA
        - MONOCHROME
        - NIGHTLIFE
        - OIL_PAINTING
        - OLD_CARTOONS
        - PAINT_GESTURE
        - POP_ART
        - RETRO_ETCHING
        - RIVIERA_POP
        - SPOTLIGHT_80S
        - STYLIZED_RED
        - SURREAL_COLLAGE
        - TRAVEL_POSTER
        - VINTAGE_GEO
        - VINTAGE_POSTER
        - WATERCOLOR
        - WEIRD
        - WOODBLOCK_PRINT
      description: >-
        A predefined style preset that applies a specific artistic style to the
        generated image.
      title: StylePresetV3
    ColorPalettePresetName:
      type: string
      enum:
        - EMBER
        - FRESH
        - JUNGLE
        - MAGIC
        - MELON
        - MOSAIC
        - PASTEL
        - ULTRAMARINE
      description: A color palette preset value.
      title: ColorPalettePresetName
    ColorPaletteWithPresetName:
      type: object
      properties:
        name:
          $ref: '#/components/schemas/ColorPalettePresetName'
      required:
        - name
      title: ColorPaletteWithPresetName
    ColorPaletteMember:
      type: object
      properties:
        color_hex:
          type: string
          description: >-
            The hexadecimal representation of the color with an optional chosen
            weight.
        color_weight:
          type: number
          format: double
          description: The weight of the color in the color palette.
      required:
        - color_hex
      description: A member of a color palette.
      title: ColorPaletteMember
    ColorPaletteWithMembers:
      type: object
      properties:
        members:
          type: array
          items:
            $ref: '#/components/schemas/ColorPaletteMember'
          description: >
            A list of ColorPaletteMembers that define the color palette. Each
            color palette member

            consists of a required color hex and an optional weight between 0.05
            and 1.0 (inclusive).

            It is recommended that these weights descend from highest to lowest
            for the color hexes provided.
      required:
        - members
      description: >-
        A color palette represented only via its members. Cannot be used in
        conjunction with preset name.
      title: ColorPaletteWithMembers
    ColorPaletteWithPresetNameOrMembers:
      oneOf:
        - $ref: '#/components/schemas/ColorPaletteWithPresetName'
        - $ref: '#/components/schemas/ColorPaletteWithMembers'
      description: >-
        A color palette for generation, must EITHER be specified via one of the
        presets (name) or explicitly via hexadecimal representations of the
        color with optional weights (members). Not supported by V_1, V_1_TURBO,
        V_2A and V_2A_TURBO models.
      title: ColorPaletteWithPresetNameOrMembers
    StyleCode:
      type: string
      description: The 8 character hexadecimal representation of the style code.
      title: StyleCode
    StyleCodes:
      type: array
      items:
        $ref: '#/components/schemas/StyleCode'
      description: >-
        A list of 8 character hexadecimal codes representing the style of the
        image. Cannot be used in conjunction with style_reference_images or
        style_type.
      title: StyleCodes
    StyleTypeV3:
      type: string
      enum:
        - AUTO
        - GENERAL
        - REALISTIC
        - DESIGN
        - FICTION
      default: GENERAL
      description: The style type to generate with.
      title: StyleTypeV3
    ImageGenerationObjectV3:
      type: object
      properties:
        url:
          type:
            - string
            - 'null'
          format: uri
          description: The direct link to the image generated.
        prompt:
          type: string
          description: >-
            The prompt used for the generation. This may be different from the
            original prompt.
        resolution:
          $ref: '#/components/schemas/ResolutionV3'
        upscaled_resolution:
          type: string
          description: >-
            Output resolution, only used if operations alters image dimensions,
            such as upscale, crop etc.
        is_image_safe:
          type: boolean
          description: >-
            Whether this request passes safety checks. If false, the url field
            will be empty.
        seed:
          type: integer
          description: Random seed. Set for reproducible generation.
        style_type:
          $ref: '#/components/schemas/StyleTypeV3'
      required:
        - prompt
        - resolution
        - is_image_safe
        - seed
      title: ImageGenerationObjectV3
    ImageGenerationResponseV3:
      type: object
      properties:
        created:
          type: string
          format: date-time
          description: The time the request was created.
        data:
          type: array
          items:
            $ref: '#/components/schemas/ImageGenerationObjectV3'
          description: A list of ImageObjects that contain the generated image(s).
      required:
        - created
        - data
      description: >-
        The response which contains information about the generated image,
        including the download link.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      title: ImageGenerationResponseV3
    GenerateImageSafetyError:
      type: object
      properties:
        error:
          type: string
      required:
        - error
      title: GenerateImageSafetyError
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Api-Key
      description: API key for access control. Use in the header with the name \"Api-Key\"

```

## Examples

**Request**

```json
{
  "image": "<file: <file1>>",
  "resolution": "512x1536",
  "style_reference_images": []
}
```

**Response**

```json
{
  "created": "2000-01-23 04:56:07+00:00",
  "data": [
    {
      "prompt": "A photo of a cat",
      "resolution": "1280x800",
      "is_image_safe": true,
      "seed": 12345,
      "url": "https://ideogram.ai/api/images/ephemeral/xtdZiqPwRxqY1Y7NExFmzB.png?exp=1743867804&sig=e13e12677633f646d8531a153d20e2d3698dca9ee7661ee5ba4f3b64e7ec3f89",
      "style_type": "GENERAL"
    }
  ]
}
```

**SDK Code**

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/reframe",
  headers={
    "Api-Key": "<apiKey>"
  },
  data={
    "resolution": "512x1536"
  },
  files={
    "image": open("<file1>", "rb"),
  }
)
print(response.json())
with open('output.png', 'wb') as f:
  f.write(requests.get(response.json()['data'][0]['url']).content)

```

```typescript
const formData = new FormData();
formData.append('resolution', '512x1536');
formData.append('image', '<file1>');
const response = await fetch('https://api.ideogram.ai/v1/ideogram-v3/reframe', {
  method: 'POST',
  headers: { 'Api-Key': '<apiKey>' },
  body: formData
});
const data = await response.json();
console.log(data);

```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://api.ideogram.ai/v1/ideogram-v3/reframe"

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Api-Key", "<apiKey>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("https://api.ideogram.ai/v1/ideogram-v3/reframe")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Api-Key"] = '<apiKey>'

response = http.request(request)
puts response.read_body
```

```java
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;

HttpResponse<String> response = Unirest.post("https://api.ideogram.ai/v1/ideogram-v3/reframe")
  .header("Api-Key", "<apiKey>")
  .asString();
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'https://api.ideogram.ai/v1/ideogram-v3/reframe', [
  'multipart' => [
    [
        'name' => 'image',
        'filename' => '<file1>',
        'contents' => null
    ],
    [
        'name' => 'resolution',
        'contents' => '512x1536'
    ]
  ]
  'headers' => [
    'Api-Key' => '<apiKey>',
  ],
]);

echo $response->getBody();
```

```csharp
using RestSharp;

var client = new RestClient("https://api.ideogram.ai/v1/ideogram-v3/reframe");
var request = new RestRequest(Method.POST);
request.AddHeader("Api-Key", "<apiKey>");
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = [
  "Api-Key": "<apiKey>",
]
let parameters = [
  [
    "name": "image",
    "fileName": "<file1>"
  ],
  [
    "name": "resolution",
    "value": "512x1536"
  ],
  [
    "name": "num_images",
    "value": 
  ],
  [
    "name": "seed",
    "value": 
  ],
  [
    "name": "rendering_speed",
    "value": 
  ],
  [
    "name": "style_preset",
    "value": 
  ],
  [
    "name": "color_palette",
    "value": 
  ],
  [
    "name": "style_codes",
    "value": 
  ]
]

var body = ""
var error: NSError? = nil
for param in parameters {
  let paramName = param["name"]!
  body += "--\(boundary)\r\n"
  body += "Content-Disposition:form-data; name=\"\(paramName)\""
  if let filename = param["fileName"] {
    let contentType = param["content-type"]!
    let fileContent = String(contentsOfFile: filename, encoding: String.Encoding.utf8)
    if (error != nil) {
      print(error as Any)
    }
    body += "; filename=\"\(filename)\"\r\n"
    body += "Content-Type: \(contentType)\r\n\r\n"
    body += fileContent
  } else if let paramValue = param["value"] {
    body += "\r\n\r\n\(paramValue)"
  }
}

let request = NSMutableURLRequest(url: NSURL(string: "https://api.ideogram.ai/v1/ideogram-v3/reframe")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "POST"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```
==================== https://developer.ideogram.ai/api-reference/api-reference/remix-v3.md ====================
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Remix with Ideogram 3.0

POST https://api.ideogram.ai/v1/ideogram-v3/remix
Content-Type: multipart/form-data

Remix provided images synchronously based on a given prompt and optional parameters with the Ideogram 3.0 model.

Input images are cropped to the chosen aspect ratio before being remixed.

Supported image formats include JPEG, PNG, and WebP.

Images links are available for a limited period of time; if you would like to keep the image, you must download it.

Reference: https://developer.ideogram.ai/api-reference/api-reference/remix-v3

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /v1/ideogram-v3/remix:
    post:
      operationId: post-remix-image-v-3
      summary: Remix with Ideogram 3.0
      description: >
        Remix provided images synchronously based on a given prompt and optional
        parameters with the Ideogram 3.0 model.

        Input images are cropped to the chosen aspect ratio before being
        remixed.

        Supported image formats include JPEG, PNG, and WebP.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      tags:
        - subpackage_generate
      parameters:
        - name: Api-Key
          in: header
          description: >-
            API key for access control. Use in the header with the name
            \"Api-Key\"
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Image(s) generated successfully.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ImageGenerationResponseV3'
        '400':
          description: Invalid input provided.
          content:
            application/json:
              schema:
                description: Any type
        '403':
          description: Not authorized to generate an image.
          content:
            application/json:
              schema:
                description: Any type
        '422':
          description: Prompt or provided image failed safety check.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/GenerateImageSafetyError'
        '429':
          description: Too many requests.
          content:
            application/json:
              schema:
                description: Any type
      requestBody:
        description: A request to remix an image with Ideogram 3.0.
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                image:
                  type: string
                  format: binary
                  description: >-
                    The image to remix binary (max size 10MB); only JPEG, WebP
                    and PNG formats are supported at this time.
                prompt:
                  type: string
                  description: The prompt to use to generate the image.
                image_weight:
                  type: integer
                  default: 50
                seed:
                  $ref: '#/components/schemas/Seed'
                resolution:
                  $ref: '#/components/schemas/ResolutionV3'
                aspect_ratio:
                  $ref: '#/components/schemas/AspectRatioV3'
                rendering_speed:
                  $ref: '#/components/schemas/RenderingSpeed'
                magic_prompt:
                  $ref: '#/components/schemas/MagicPromptOption'
                negative_prompt:
                  type: string
                  description: >
                    Description of what to exclude from an image. Descriptions
                    in the prompt take precedence

                    to descriptions in the negative prompt.
                num_images:
                  type: integer
                  default: 1
                  description: Number of images to generate.
                color_palette:
                  $ref: '#/components/schemas/ColorPaletteWithPresetNameOrMembers'
                style_codes:
                  $ref: '#/components/schemas/StyleCodes'
                style_type:
                  $ref: '#/components/schemas/StyleTypeV3'
                style_preset:
                  $ref: '#/components/schemas/StylePresetV3'
                style_reference_images:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    A set of images to use as style references (maximum total
                    size 10MB across all style references). The images should be
                    in JPEG, PNG or WebP format.
                character_reference_images:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    Generations with character reference are subject to the
                    character reference pricing. A set of images to use as
                    character references (maximum total size 10MB across all
                    character references), currently only supports 1 character
                    reference image. The images should be in JPEG, PNG or WebP
                    format.
                character_reference_images_mask:
                  type: array
                  items:
                    type: string
                    format: binary
                  description: >-
                    Optional masks for character reference images. When
                    provided, must match the number of
                    character_reference_images. Each mask should be a grayscale
                    image of the same dimensions as the corresponding character
                    reference image. The images should be in JPEG, PNG or WebP
                    format.
              required:
                - image
                - prompt
servers:
  - url: https://api.ideogram.ai
    description: https://api.ideogram.ai
components:
  schemas:
    Seed:
      type: integer
      description: Random seed. Set for reproducible generation.
      title: Seed
    ResolutionV3:
      type: string
      enum:
        - 512x1536
        - 576x1408
        - 576x1472
        - 576x1536
        - 640x1344
        - 640x1408
        - 640x1472
        - 640x1536
        - 704x1152
        - 704x1216
        - 704x1280
        - 704x1344
        - 704x1408
        - 704x1472
        - 736x1312
        - 768x1088
        - 768x1216
        - 768x1280
        - 768x1344
        - 800x1280
        - 832x960
        - 832x1024
        - 832x1088
        - 832x1152
        - 832x1216
        - 832x1248
        - 864x1152
        - 896x960
        - 896x1024
        - 896x1088
        - 896x1120
        - 896x1152
        - 960x832
        - 960x896
        - 960x1024
        - 960x1088
        - 1024x832
        - 1024x896
        - 1024x960
        - 1024x1024
        - 1088x768
        - 1088x832
        - 1088x896
        - 1088x960
        - 1120x896
        - 1152x704
        - 1152x832
        - 1152x864
        - 1152x896
        - 1216x704
        - 1216x768
        - 1216x832
        - 1248x832
        - 1280x704
        - 1280x768
        - 1280x800
        - 1312x736
        - 1344x640
        - 1344x704
        - 1344x768
        - 1408x576
        - 1408x640
        - 1408x704
        - 1472x576
        - 1472x640
        - 1472x704
        - 1536x512
        - 1536x576
        - 1536x640
      description: The resolutions supported for Ideogram 3.0.
      title: ResolutionV3
    AspectRatioV3:
      type: string
      enum:
        - 1x3
        - 3x1
        - 1x2
        - 2x1
        - 9x16
        - 16x9
        - 10x16
        - 16x10
        - 2x3
        - 3x2
        - 3x4
        - 4x3
        - 4x5
        - 5x4
        - 1x1
      description: >-
        The aspect ratio to use for image generation, which determines the
        image's resolution. Cannot be used in conjunction with resolution.
        Defaults to 1x1.
      title: AspectRatioV3
    RenderingSpeed:
      type: string
      enum:
        - FLASH
        - TURBO
        - DEFAULT
        - QUALITY
      default: DEFAULT
      description: The rendering speed to use.
      title: RenderingSpeed
    MagicPromptOption:
      type: string
      enum:
        - AUTO
        - 'ON'
        - 'OFF'
      description: >-
        Determine if MagicPrompt should be used in generating the request or
        not.
      title: MagicPromptOption
    ColorPalettePresetName:
      type: string
      enum:
        - EMBER
        - FRESH
        - JUNGLE
        - MAGIC
        - MELON
        - MOSAIC
        - PASTEL
        - ULTRAMARINE
      description: A color palette preset value.
      title: ColorPalettePresetName
    ColorPaletteWithPresetName:
      type: object
      properties:
        name:
          $ref: '#/components/schemas/ColorPalettePresetName'
      required:
        - name
      title: ColorPaletteWithPresetName
    ColorPaletteMember:
      type: object
      properties:
        color_hex:
          type: string
          description: >-
            The hexadecimal representation of the color with an optional chosen
            weight.
        color_weight:
          type: number
          format: double
          description: The weight of the color in the color palette.
      required:
        - color_hex
      description: A member of a color palette.
      title: ColorPaletteMember
    ColorPaletteWithMembers:
      type: object
      properties:
        members:
          type: array
          items:
            $ref: '#/components/schemas/ColorPaletteMember'
          description: >
            A list of ColorPaletteMembers that define the color palette. Each
            color palette member

            consists of a required color hex and an optional weight between 0.05
            and 1.0 (inclusive).

            It is recommended that these weights descend from highest to lowest
            for the color hexes provided.
      required:
        - members
      description: >-
        A color palette represented only via its members. Cannot be used in
        conjunction with preset name.
      title: ColorPaletteWithMembers
    ColorPaletteWithPresetNameOrMembers:
      oneOf:
        - $ref: '#/components/schemas/ColorPaletteWithPresetName'
        - $ref: '#/components/schemas/ColorPaletteWithMembers'
      description: >-
        A color palette for generation, must EITHER be specified via one of the
        presets (name) or explicitly via hexadecimal representations of the
        color with optional weights (members). Not supported by V_1, V_1_TURBO,
        V_2A and V_2A_TURBO models.
      title: ColorPaletteWithPresetNameOrMembers
    StyleCode:
      type: string
      description: The 8 character hexadecimal representation of the style code.
      title: StyleCode
    StyleCodes:
      type: array
      items:
        $ref: '#/components/schemas/StyleCode'
      description: >-
        A list of 8 character hexadecimal codes representing the style of the
        image. Cannot be used in conjunction with style_reference_images or
        style_type.
      title: StyleCodes
    StyleTypeV3:
      type: string
      enum:
        - AUTO
        - GENERAL
        - REALISTIC
        - DESIGN
        - FICTION
      default: GENERAL
      description: The style type to generate with.
      title: StyleTypeV3
    StylePresetV3:
      type: string
      enum:
        - 80S_ILLUSTRATION
        - 90S_NOSTALGIA
        - ABSTRACT_ORGANIC
        - ANALOG_NOSTALGIA
        - ART_BRUT
        - ART_DECO
        - ART_POSTER
        - AURA
        - AVANT_GARDE
        - BAUHAUS
        - BLUEPRINT
        - BLURRY_MOTION
        - BRIGHT_ART
        - C4D_CARTOON
        - CHILDRENS_BOOK
        - COLLAGE
        - COLORING_BOOK_I
        - COLORING_BOOK_II
        - CUBISM
        - DARK_AURA
        - DOODLE
        - DOUBLE_EXPOSURE
        - DRAMATIC_CINEMA
        - EDITORIAL
        - EMOTIONAL_MINIMAL
        - ETHEREAL_PARTY
        - EXPIRED_FILM
        - FLAT_ART
        - FLAT_VECTOR
        - FOREST_REVERIE
        - GEO_MINIMALIST
        - GLASS_PRISM
        - GOLDEN_HOUR
        - GRAFFITI_I
        - GRAFFITI_II
        - HALFTONE_PRINT
        - HIGH_CONTRAST
        - HIPPIE_ERA
        - ICONIC
        - JAPANDI_FUSION
        - JAZZY
        - LONG_EXPOSURE
        - MAGAZINE_EDITORIAL
        - MINIMAL_ILLUSTRATION
        - MIXED_MEDIA
        - MONOCHROME
        - NIGHTLIFE
        - OIL_PAINTING
        - OLD_CARTOONS
        - PAINT_GESTURE
        - POP_ART
        - RETRO_ETCHING
        - RIVIERA_POP
        - SPOTLIGHT_80S
        - STYLIZED_RED
        - SURREAL_COLLAGE
        - TRAVEL_POSTER
        - VINTAGE_GEO
        - VINTAGE_POSTER
        - WATERCOLOR
        - WEIRD
        - WOODBLOCK_PRINT
      description: >-
        A predefined style preset that applies a specific artistic style to the
        generated image.
      title: StylePresetV3
    ImageGenerationObjectV3:
      type: object
      properties:
        url:
          type:
            - string
            - 'null'
          format: uri
          description: The direct link to the image generated.
        prompt:
          type: string
          description: >-
            The prompt used for the generation. This may be different from the
            original prompt.
        resolution:
          $ref: '#/components/schemas/ResolutionV3'
        upscaled_resolution:
          type: string
          description: >-
            Output resolution, only used if operations alters image dimensions,
            such as upscale, crop etc.
        is_image_safe:
          type: boolean
          description: >-
            Whether this request passes safety checks. If false, the url field
            will be empty.
        seed:
          type: integer
          description: Random seed. Set for reproducible generation.
        style_type:
          $ref: '#/components/schemas/StyleTypeV3'
      required:
        - prompt
        - resolution
        - is_image_safe
        - seed
      title: ImageGenerationObjectV3
    ImageGenerationResponseV3:
      type: object
      properties:
        created:
          type: string
          format: date-time
          description: The time the request was created.
        data:
          type: array
          items:
            $ref: '#/components/schemas/ImageGenerationObjectV3'
          description: A list of ImageObjects that contain the generated image(s).
      required:
        - created
        - data
      description: >-
        The response which contains information about the generated image,
        including the download link.

        Images links are available for a limited period of time; if you would
        like to keep the image, you must download it.
      title: ImageGenerationResponseV3
    GenerateImageSafetyError:
      type: object
      properties:
        error:
          type: string
      required:
        - error
      title: GenerateImageSafetyError
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: Api-Key
      description: API key for access control. Use in the header with the name \"Api-Key\"

```

## Examples

**Request**

```json
{
  "image": "<file: <file1>>",
  "prompt": "A photo of a cat",
  "image_weight": 50,
  "aspect_ratio": "1x2",
  "rendering_speed": "DEFAULT",
  "style_type": "AUTO",
  "style_reference_images": [],
  "character_reference_images": [],
  "character_reference_images_mask": []
}
```

**Response**

```json
{
  "created": "2000-01-23 04:56:07+00:00",
  "data": [
    {
      "prompt": "A photo of a cat",
      "resolution": "1280x800",
      "is_image_safe": true,
      "seed": 12345,
      "url": "https://ideogram.ai/api/images/ephemeral/xtdZiqPwRxqY1Y7NExFmzB.png?exp=1743867804&sig=e13e12677633f646d8531a153d20e2d3698dca9ee7661ee5ba4f3b64e7ec3f89",
      "style_type": "GENERAL"
    }
  ]
}
```

**SDK Code**

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/remix",
  headers={
    "Api-Key": "<apiKey>"
  },
  data={
    "prompt": "A photo of a cat",
    "rendering_speed": "TURBO"
  },
  files={
    "image": open("<file1>", "rb"),
  }
)
print(response.json())
with open('output.png', 'wb') as f:
  f.write(requests.get(response.json()['data'][0]['url']).content)

```

```typescript
const formData = new FormData();
formData.append('prompt', 'A photo of a cat');
formData.append('rendering_speed', 'TURBO');
formData.append('image', '<file1>');
const response = await fetch('https://api.ideogram.ai/v1/ideogram-v3/remix', {
  method: 'POST',
  headers: { 'Api-Key': '<apiKey>' },
  body: formData
});
const data = await response.json();
console.log(data);

```

```go
package main

import (
	"fmt"
	"strings"
	"net/http"
	"io"
)

func main() {

	url := "https://api.ideogram.ai/v1/ideogram-v3/remix"

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Api-Key", "<apiKey>")

	res, _ := http.DefaultClient.Do(req)

	defer res.Body.Close()
	body, _ := io.ReadAll(res.Body)

	fmt.Println(res)
	fmt.Println(string(body))

}
```

```ruby
require 'uri'
require 'net/http'

url = URI("https://api.ideogram.ai/v1/ideogram-v3/remix")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Api-Key"] = '<apiKey>'

response = http.request(request)
puts response.read_body
```

```java
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;

HttpResponse<String> response = Unirest.post("https://api.ideogram.ai/v1/ideogram-v3/remix")
  .header("Api-Key", "<apiKey>")
  .asString();
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'https://api.ideogram.ai/v1/ideogram-v3/remix', [
  'multipart' => [
    [
        'name' => 'image',
        'filename' => '<file1>',
        'contents' => null
    ],
    [
        'name' => 'prompt',
        'contents' => 'A photo of a cat'
    ],
    [
        'name' => 'image_weight',
        'contents' => '50'
    ],
    [
        'name' => 'aspect_ratio',
        'contents' => '1x2'
    ],
    [
        'name' => 'rendering_speed',
        'contents' => 'DEFAULT'
    ],
    [
        'name' => 'style_type',
        'contents' => 'AUTO'
    ]
  ]
  'headers' => [
    'Api-Key' => '<apiKey>',
  ],
]);

echo $response->getBody();
```

```csharp
using RestSharp;

var client = new RestClient("https://api.ideogram.ai/v1/ideogram-v3/remix");
var request = new RestRequest(Method.POST);
request.AddHeader("Api-Key", "<apiKey>");
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = [
  "Api-Key": "<apiKey>",
]
let parameters = [
  [
    "name": "image",
    "fileName": "<file1>"
  ],
  [
    "name": "prompt",
    "value": "A photo of a cat"
  ],
  [
    "name": "image_weight",
    "value": "50"
  ],
  [
    "name": "seed",
    "value": 
  ],
  [
    "name": "resolution",
    "value": 
  ],
  [
    "name": "aspect_ratio",
    "value": "1x2"
  ],
  [
    "name": "rendering_speed",
    "value": "DEFAULT"
  ],
  [
    "name": "magic_prompt",
    "value": 
  ],
  [
    "name": "negative_prompt",
    "value": 
  ],
  [
    "name": "num_images",
    "value": 
  ],
  [
    "name": "color_palette",
    "value": 
  ],
  [
    "name": "style_codes",
    "value": 
  ],
  [
    "name": "style_type",
    "value": "AUTO"
  ],
  [
    "name": "style_preset",
    "value": 
  ]
]

var body = ""
var error: NSError? = nil
for param in parameters {
  let paramName = param["name"]!
  body += "--\(boundary)\r\n"
  body += "Content-Disposition:form-data; name=\"\(paramName)\""
  if let filename = param["fileName"] {
    let contentType = param["content-type"]!
    let fileContent = String(contentsOfFile: filename, encoding: String.Encoding.utf8)
    if (error != nil) {
      print(error as Any)
    }
    body += "; filename=\"\(filename)\"\r\n"
    body += "Content-Type: \(contentType)\r\n\r\n"
    body += fileContent
  } else if let paramValue = param["value"] {
    body += "\r\n\r\n\(paramValue)"
  }
}

let request = NSMutableURLRequest(url: NSURL(string: "https://api.ideogram.ai/v1/ideogram-v3/remix")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "POST"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```
==================== https://developer.ideogram.ai/tutorials/custom-model-training.md ====================
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Custom Model Training

Train a custom model on your own images, then use it to generate new images in your unique style.

## Overview

Custom model training lets you fine-tune an Ideogram model on your own dataset of images. Once training completes, you can use the model with the **Generate** endpoint by passing its `custom_model_uri`.

The workflow has four steps:

1. **Create a dataset** to hold your training images.
2. **Upload images** (and optional captions) to the dataset.
3. **Start training** to kick off the model training job.
4. **Generate images** using your trained model.

## Step 1: Create a Dataset

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/datasets",
  headers={"Api-Key": "<apiKey>"},
  json={"name": "My Training Dataset"}
)
dataset = response.json()
dataset_id = dataset["dataset_id"]
print(f"Created dataset: {dataset_id}")
```

```bash
curl -X POST https://api.ideogram.ai/datasets \
  -H "Api-Key: <apiKey>" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Training Dataset"}'
```

## Step 2: Upload Training Images

Upload your training images to the dataset. You can upload individual images (JPEG, PNG, WebP), optional `.txt` caption sidecar files, or ZIP archives containing both.

* A dataset needs **at least 10 images** to start training.
* A dataset can hold **up to 100 images**.
* Caption files are matched by filename stem (e.g. `sunset.txt` captions `sunset.jpg`).

```python
import requests
import glob

# Upload individual images
files = [("files", open(f, "rb")) for f in glob.glob("training_images/*.jpg")]

response = requests.post(
  f"https://api.ideogram.ai/datasets/{dataset_id}/upload_assets",
  headers={"Api-Key": "<apiKey>"},
  files=files
)
result = response.json()
print(f"Uploaded {result['success_count']}/{result['total_count']} images")
```

```bash
curl -X POST https://api.ideogram.ai/datasets/<dataset_id>/upload_assets \
  -H "Api-Key: <apiKey>" \
  -H "Content-Type: multipart/form-data" \
  -F files=@image1.jpg \
  -F files=@image2.jpg \
  -F files=@image3.jpg
```

You can also upload a ZIP file containing images and captions together, which is convenient for larger datasets.

## Step 3: Train the Model

Once your dataset has enough images, start training by giving your model a name.

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/train-model",
  headers={"Api-Key": "<apiKey>"},
  json={"dataset_id": dataset_id, "model_name": "my-custom-model"}
)
training = response.json()
model_id = training["model_id"]
print(f"Training started: {training['training_status']}")
```

```bash
curl -X POST https://api.ideogram.ai/v1/ideogram-v3/train-model \
  -H "Api-Key: <apiKey>" \
  -H "Content-Type: application/json" \
  -d '{"dataset_id": "<dataset_id>", "model_name": "my-custom-model"}'
```

## Checking Training Status

Poll the model details endpoint to check when training completes.

```python
import requests
import time

while True:
  response = requests.get(
    f"https://api.ideogram.ai/models/{model_id}",
    headers={"Api-Key": "<apiKey>"}
  )
  model = response.json()["model"]
  print(f"Status: {model['status']}")

  if model["status"] == "COMPLETED":
    print(f"Model ready! URI: {model.get('custom_model_uri')}")
    break
  elif model["status"] == "ERRORED":
    print("Training failed.")
    break

  time.sleep(60)
```

```bash
curl -X GET https://api.ideogram.ai/models/<model_id> \
  -H "Api-Key: <apiKey>"
```

## Step 4: Generate with Your Model

Once training is complete and `is_available_for_generation` is `true`, use the `custom_model_uri` from the model details to generate images.

```python
import requests

response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/generate",
  headers={"Api-Key": "<apiKey>"},
  data={
    "prompt": "A photo in my custom style",
    "custom_model_uri": "model/my-custom-model/version/1",
    "rendering_speed": "DEFAULT"
  }
)
result = response.json()
if response.status_code == 200:
  print(result["data"][0]["url"])
```

```bash
curl -X POST https://api.ideogram.ai/v1/ideogram-v3/generate \
  -H "Api-Key: <apiKey>" \
  -H "Content-Type: multipart/form-data" \
  -F prompt="A photo in my custom style" \
  -F custom_model_uri="model/my-custom-model/version/1" \
  -F rendering_speed="DEFAULT"
```

## Tips for Better Results

* **Use high-quality images** that clearly represent the style or subject you want the model to learn.
* **Add captions** to guide the model on what each image represents. Captions are optional!
* **Use consistent subjects** across your training images for best results with style transfer.
==================== https://developer.ideogram.ai/api-reference/custom-model-training/train-v3-model.md ====================
# Page Not Found

This page does not exist.

==================== https://developer.ideogram.ai/ideogram-api/api-overview.md ====================
> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Ideogram Developer API

The Ideogram API lets you integrate the Ideogram Image Generation models right into your product.

## Capabilities

Prompt fidelity, crystal-clear type, reliable editing, and production-ready image workflows across the app, API, MCP, and open weights.

Remove a background for a transparent cutout, or replace it with a generated scene from a prompt.

Ideogram excels at integrating text into images for logos, branding, POD, or design layouts.

Train on-brand image models from your approved assets so generations follow your style, art direction, typography, and visual identity.

### Generate

Generate an image given a descriptive prompt.

*prompt: A photo of a cat sleeping on a couch.*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/c4175df52dae484a097361fe9cf6d1a5447c1ef6e12a6c9b8845de4d60cf3657/assets/API_Generate_Cat_Sleeping.png" width="355" height="200" />

### Remix

The **Remix** tool is invaluable for making changes to an existing image, whether it was generated in Ideogram or uploaded. The AI uses the original image as a basis to generate a new one, allowing you to control how much influence the original image has on the final result.

*prompt: A photo of a dog sleeping on a couch*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/44ee41021866594fa57b3f09d6ae59ead087696adc75d74d7cc581a9624e9773/assets/API_Remix_Cat_Sleeping.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/277a53d25343c498715d48729bbd51b3a4a3a3acba0bc61d22169b502d0267ee/assets/API_Remix_Dog_Sleeping.png" width="200" height="200" />

### Edit

Take a starting image and modify a part of an image while keeping the rest intact.

*prompt: A dog wearing a cowboy hat*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/a0ec5ec44044270b41926319dc759d04f72223ff56d3c7c3fb515fcf54c3165c/assets/API_Edit_Dog_Input.jpeg" width="173" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/e48bfa22968f270ac136fd12243f73cad9246aacecfbb2b115ac1e1bbc06c018/assets/API_Edit_Mask.jpeg" width="173" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/523005bb829cfbcd72a666c3d38d6a57ab729380c2f91459f5f06a45ec78dcce/assets/API_Edit_Result.png" width="173" height="200" />

### Reframe

Take a starting image and extend it to match your desired resolution.

*resolution: 1280x768*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/ee072c3d9d9b592b8f97597acee0e04f09f2b52c57cd43d6ee6f1bda1f7e7a49/assets/API_Character_Result.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/97a10963e47d8df6bebac168ea2691cb40021fa45c60e614b6f4c425d099af0d/assets/API_Reframe_Result.png" width="333" height="200" />

### Replace Background

Take a starting image and replace the background with a new one.

*prompt: A man standing in a busy coffee shop*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/7e5374e84f8394a1d41cd52e89041e698689167455b63552fdc911a9ea4a000e/assets/API_Character.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/256b57fd5837cb20a23e5ceb64d95d8ede925100c5174b60ab27ab8ba3ec6a08/assets/API_Replace_Background_Result.png" width="200" height="200" />

### Face Swapping

Using the Edit endpoint, you can take a starting image and swap the face of the person in the image with a new one.

*prompt: A man sitting on a motorcycle in a dimly lit garage*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/ee072c3d9d9b592b8f97597acee0e04f09f2b52c57cd43d6ee6f1bda1f7e7a49/assets/API_Character_Result.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/d651067950c2440063d3b3de14c7fc0db0b908d4d9afcbe64737003a34104d89/assets/API_Edit_Character_Mask.jpeg" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/1f68e2f04e44d61a0bdcf442c7c5811666a802df5a8748380a17456db128644d/assets/API_Edit_Character.jpeg" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/687c40bb58485c9b5abed3b53016e474d2444b2ce9293e94a544a8afd0b74d00/assets/API_Edit_Character_Result.png" width="200" height="200" />

### Style Presets

Using any of the API V3 endpoints, you can use a style\_preset to generate an image.
Here are a few examples with the same prompt but different `style_preset` values.

*prompt: A bioluminescent jellyfish in an underwater city*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/2b11d4d32347cc5f3e69c42494b56d36dbe8ec8491dea608ac06dc6eee9e3dce/assets/jellyfish_90s_nostalgia.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/12b8f317a306fef79b5e55e2ff92e77a995a79ce17caa1afda6dd5956f63be7a/assets/jellyfish_japandi.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/c2732f7412111b09e448c6c02a51fd431a115c7504fc47a6cc6436f5ca84e67c/assets/jellyfish_mixed_media.png" width="200" height="200" />

*prompt: A birthday cake with "Creative Typography" written on it*

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/29e301fcc47f944e510684bc94dbd38e796270bac368bd172038c7398c97fc0c/assets/typography_80s_spotlight.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/d47774b14978f9f1bf4758fcbd0cee2ecf44729331bd6533f648e70f7ecf6af5/assets/typography_art_brut.png" width="200" height="200" />

<img src="https://files.buildwithfern.com/https://ideogram.docs.buildwithfern.com/236d24c3871287635f520f726bb9ce54a467a9fa4331df091565960128f75c02/assets/typography_c4d_cartoon.png" width="200" height="200" />

For more detailed documentation on our models' capabilities, please refer to our [Official Documentation](https://docs.ideogram.ai/).

## Start building

Get started by following our Setup guide and then follow this example for a simple Generation with and without character reference.

View the full API reference for all endpoints and parameters.

## Quickstart

Get started by following our Setup guide and then follow this example for a simple Generation with and without a character reference image.

```python
import requests

# Generate with Ideogram 3.0 (POST /v1/ideogram-v3/generate)
response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/generate",
  headers={
    "Api-Key": "<apiKey>"
  },
  json={
    "prompt": "A picture of a cat",
    "rendering_speed": "TURBO"
  }
)
print(response.json())
if response.status_code == 200:
  with open('output.png', 'wb') as f:
    f.write(requests.get(response.json()['data'][0]['url']).content)

# Generate with character reference
response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/generate",
  headers={
    "Api-Key": "<apiKey>"
  },
  data={
    "style_type": "AUTO",
    "prompt": "A cinematic medium shot of a man sitting on a motorcycle in a dimly lit garage.",
  },
  files=[
    ("character_reference_images", open("character_reference_image.png", "rb")),
  ]
)
print(response.json())
if response.status_code == 200:
  with open('output_character.png', 'wb') as f:
    f.write(requests.get(response.json()['data'][0]['url']).content)
```

```typescript
const formData = new FormData();
formData.append('prompt', 'A photo of a cat');
formData.append('rendering_speed', 'TURBO');
formData.append('style_type', 'AUTO');

// To add character reference images, uncomment the following lines
// formData.append('character_reference_images', '<character_reference_image>');
const response = await fetch('https://api.ideogram.ai/v1/ideogram-v3/generate', {
  method: 'POST',
  headers: { 'Api-Key': '<apiKey>' },
  body: formData
});
const data = await response.json();
console.log(data);
```

## Enterprise Scale

The Ideogram API serves thousands of API customers to generate millions of images daily. If you wish to utilize our API at a larger scale than our default rate limit of 10 inflight requests, please reach out to us at *[partnership@ideogram.ai](mailto:partnership@ideogram.ai)* and we will help fit your exact needs.