> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://developer.ideogram.ai/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://developer.ideogram.ai/_mcp/server.

# Generate with Ideogram 3.0

POST https://api.ideogram.ai/v1/ideogram-v3/generate
Content-Type: multipart/form-data

Generates images synchronously based on a given prompt and optional parameters using the Ideogram 3.0 model.

Images links are available for a limited period of time; if you would like to keep the image, you must download it.


Reference: https://developer.ideogram.ai/api-reference/api-reference/generate-v3

## OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: API
  version: 1.0.0
paths:
  /v1/ideogram-v3/generate:
    post:
      operationId: post-generate-image-v-3
      summary: Generate with Ideogram 3.0
      description: >
        Generates images synchronously based on a given prompt and optional
        parameters using the Ideogram 3.0 model.


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
        '401':
          description: Not authorized to generate an image.
          content:
            application/json:
              schema:
                description: Any type
        '422':
          description: Prompt failed the safety check.
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
        description: A request to generate an image with Ideogram 3.0.
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                prompt:
                  type: string
                  description: The prompt to use to generate the image.
                seed:
                  type: integer
                  description: Random seed. Set for reproducible generation.
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
                  type: array
                  items:
                    $ref: '#/components/schemas/StyleCode'
                  description: >-
                    A list of 8 character hexadecimal codes representing the
                    style of the image. Cannot be used in conjunction with
                    style_reference_images or style_type.
                style_type:
                  $ref: '#/components/schemas/StyleTypeV3'
                style_preset:
                  $ref: '#/components/schemas/StylePresetV3'
                custom_model_uri:
                  type: string
                  description: >
                    A custom model URI in the format
                    model/<model_name>/version/<version_name>. 

                    When provided, the model version and style will be resolved
                    from this URI, and style_type is not required.
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
                enable_copyright_detection:
                  type:
                    - boolean
                    - 'null'
                  description: >
                    Optional. Opt this request into post-generation copyright
                    detection (Hive likeness + logo

                    checks). The effective gate is the OR of this field and the
                    organization's

                    `copyright_detection_enabled` setting on `/api`: if the org
                    has it on, this is ignored;

                    if the org has it off, setting this `true` enables detection
                    for this request only.

                    Adds detection latency. Flagged images come back with
                    `is_image_safe: false`.
              required:
                - prompt
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
  "prompt": "A photo of a cat sleeping on a couch.",
  "aspect_ratio": "1x1",
  "rendering_speed": "TURBO",
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
      "prompt": "A photo of a cat sleeping on a couch.",
      "resolution": "1024x1024",
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
with open('output.png', 'wb') as f:
  f.write(requests.get(response.json()['data'][0]['url']).content)

# Generate with style reference images
response = requests.post(
  "https://api.ideogram.ai/v1/ideogram-v3/generate",
  headers={
    "Api-Key": "<apiKey>"
  },
  data={
    "prompt": "A picture of a cat",
    "aspect_ratio": "3x1"
  },
  files=[
    ("style_reference_images", open("style_reference_image_1.png", "rb")),
    ("style_reference_images", open("style_reference_image_2.png", "rb")),
  ]
)
print(response.json())
with open('output.png', 'wb') as f:
  f.write(requests.get(response.json()['data'][0]['url']).content)

```

```typescript
const formData = new FormData();
formData.append('prompt', 'A photo of a cat');
formData.append('rendering_speed', 'TURBO');
// To add style reference images, uncomment the following lines
// formData.append('style_reference_images', '<style_reference_image_1>');
// formData.append('style_reference_images', '<style_reference_image_2>');
const response = await fetch('https://api.ideogram.ai/v1/ideogram-v3/generate', {
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

	url := "https://api.ideogram.ai/v1/ideogram-v3/generate"

	payload := strings.NewReader("-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\nA photo of a cat sleeping on a couch.\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"seed\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"resolution\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"aspect_ratio\"\r\n\r\n1x1\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"rendering_speed\"\r\n\r\nTURBO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"magic_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"negative_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"num_images\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"color_palette\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_codes\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_type\"\r\n\r\nAUTO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_preset\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"custom_model_uri\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"enable_copyright_detection\"\r\n\r\n\r\n-----011000010111000001101001--\r\n")

	req, _ := http.NewRequest("POST", url, payload)

	req.Header.Add("Api-Key", "<apiKey>")
	req.Header.Add("Content-Type", "multipart/form-data; boundary=---011000010111000001101001")

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

url = URI("https://api.ideogram.ai/v1/ideogram-v3/generate")

http = Net::HTTP.new(url.host, url.port)
http.use_ssl = true

request = Net::HTTP::Post.new(url)
request["Api-Key"] = '<apiKey>'
request["Content-Type"] = 'multipart/form-data; boundary=---011000010111000001101001'
request.body = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\nA photo of a cat sleeping on a couch.\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"seed\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"resolution\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"aspect_ratio\"\r\n\r\n1x1\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"rendering_speed\"\r\n\r\nTURBO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"magic_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"negative_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"num_images\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"color_palette\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_codes\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_type\"\r\n\r\nAUTO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_preset\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"custom_model_uri\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"enable_copyright_detection\"\r\n\r\n\r\n-----011000010111000001101001--\r\n"

response = http.request(request)
puts response.read_body
```

```java
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.Unirest;

HttpResponse<String> response = Unirest.post("https://api.ideogram.ai/v1/ideogram-v3/generate")
  .header("Api-Key", "<apiKey>")
  .header("Content-Type", "multipart/form-data; boundary=---011000010111000001101001")
  .body("-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\nA photo of a cat sleeping on a couch.\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"seed\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"resolution\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"aspect_ratio\"\r\n\r\n1x1\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"rendering_speed\"\r\n\r\nTURBO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"magic_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"negative_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"num_images\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"color_palette\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_codes\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_type\"\r\n\r\nAUTO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_preset\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"custom_model_uri\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"enable_copyright_detection\"\r\n\r\n\r\n-----011000010111000001101001--\r\n")
  .asString();
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'https://api.ideogram.ai/v1/ideogram-v3/generate', [
  'multipart' => [
    [
        'name' => 'prompt',
        'contents' => 'A photo of a cat sleeping on a couch.'
    ],
    [
        'name' => 'aspect_ratio',
        'contents' => '1x1'
    ],
    [
        'name' => 'rendering_speed',
        'contents' => 'TURBO'
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

var client = new RestClient("https://api.ideogram.ai/v1/ideogram-v3/generate");
var request = new RestRequest(Method.POST);
request.AddHeader("Api-Key", "<apiKey>");
request.AddParameter("multipart/form-data; boundary=---011000010111000001101001", "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"prompt\"\r\n\r\nA photo of a cat sleeping on a couch.\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"seed\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"resolution\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"aspect_ratio\"\r\n\r\n1x1\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"rendering_speed\"\r\n\r\nTURBO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"magic_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"negative_prompt\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"num_images\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"color_palette\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_codes\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_type\"\r\n\r\nAUTO\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"style_preset\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"custom_model_uri\"\r\n\r\n\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"enable_copyright_detection\"\r\n\r\n\r\n-----011000010111000001101001--\r\n", ParameterType.RequestBody);
IRestResponse response = client.Execute(request);
```

```swift
import Foundation

let headers = [
  "Api-Key": "<apiKey>",
  "Content-Type": "multipart/form-data; boundary=---011000010111000001101001"
]
let parameters = [
  [
    "name": "prompt",
    "value": "A photo of a cat sleeping on a couch."
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
    "value": "1x1"
  ],
  [
    "name": "rendering_speed",
    "value": "TURBO"
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
  ],
  [
    "name": "custom_model_uri",
    "value": 
  ],
  [
    "name": "enable_copyright_detection",
    "value": 
  ]
]

let boundary = "---011000010111000001101001"

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

let request = NSMutableURLRequest(url: NSURL(string: "https://api.ideogram.ai/v1/ideogram-v3/generate")! as URL,
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