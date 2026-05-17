# GeoPrompt Urban Scenario Visualizer

AI-powered georeferenced urban scenario visualization plugin for QGIS.

**Created by Firman Afrianto and Maya Safira**

## What this plugin does

GeoPrompt Urban Scenario Visualizer converts a selected QGIS map canvas or extent into an image, sends it to an image-generation or image-editing provider, then writes the generated result back into QGIS as a georeferenced GeoTIFF layer.

The plugin is intended for urban and regional planning communication, design exploration, and scenario visualization. It is not intended for official legal mapping, parcel delineation, survey-grade measurement, or authoritative land-use classification.

## Supported providers

1. **OpenAI**
   - Recommended default: `gpt-image-1.5`
   - Additional options: `gpt-image-1`, `gpt-image-1-mini`, `gpt-image-2`, `chatgpt-image-latest`, `dall-e-2`, and custom model ID.

2. **Google Gemini Image**
   - `gemini-2.5-flash-image`
   - `gemini-3-pro-image-preview`
   - Custom Gemini model ID.

## Main workflow

1. Open a QGIS project and load basemap, raster, vector, or XYZ tile layers.
2. Open **GeoPrompt Urban Scenario Visualizer**.
3. Select a provider: **OpenAI** or **Google Gemini Image**.
4. Paste the relevant API key.
5. Select a model.
6. Choose one of the urban and regional planning prompt presets or write a custom prompt.
7. Choose output size and quality.
8. Select an area on the QGIS canvas or use the current canvas extent.
9. Click **Generate GeoPrompt Scenario**.
10. The plugin exports the selected canvas area, sends it to the provider, receives the generated image, crops padding if needed, converts it to a georeferenced GeoTIFF, and loads it into the QGIS Layers Panel.

## Planning terminology used in the plugin

The plugin uses English planning terminology for broader international readability:

- **Detailed Spatial Plan** refers to detailed zoning or detailed land-use planning.
- **Strategic Environmental Assessment** refers to environmental assessment for plans, policies, and programs.
- **Urban and Regional Planning** refers to spatial planning, urban planning, and regional planning workflows.
- **Transit-Oriented Development** refers to compact mixed-use development around transit corridors and nodes.

## Key capabilities

- Curated urban and regional planning prompt presets.
- Preserve-geometry mode.
- Ratio-locked selection.
- Automatic padding and crop alignment.
- Direct loading into the QGIS Layers Panel.
- Optional zoom-to-result.
- Provider switching.
- Custom model ID support.
- Output GeoTIFF metadata embedding.

## Dependencies

Install the OpenAI and Google GenAI Python packages inside the QGIS Python environment:

```bash
python -m pip install openai google-genai Pillow
```

The plugin also uses GDAL and Qt classes already available in QGIS.

## Important warning

Generated outputs are AI scenario visualizations. They are not official spatial data and must not be used for legal delineation, measurement, or authoritative classification without validation.

## Version 1.0.0 changes

- Improved no-zoom alignment behavior by strengthening preserve-geometry prompts with explicit full-frame, no-crop, no-zoom, no-rescale instructions.
- Set automatic padding to off by default because provider-side image reframing can make generated outputs appear slightly zoomed when padding is cropped back.
- Added clearer UI guidance: best overlay alignment is achieved with locked selection ratio and automatic padding disabled.
- Added 20 more prompt presets, including 10 mobility and accessibility presets and 10 land-use, zoning, and development-control presets aligned with current urban planning practice.
- Reorganized all presets into Basic, Intermediate, and Advanced categories for easier navigation.
- Reduced the subtitle and creator-line font size in the plugin header for a cleaner dock layout.
- Added 10 new prompt presets aligned with current urban planning trends, including 15-minute neighborhoods, sponge city design, net-zero districts, complete streets, resilience hubs, walkability, heat-risk prioritization, blue-green structure planning, and inclusive public realm scenarios.
- Converted all plugin UI text, status messages, error messages, README content, metadata, and prompt presets into English.
- Replaced Indonesian planning abbreviations with internationally readable planning terms.
- Cleaned old changelog clutter from earlier development versions.
- Kept only the stable provider paths: OpenAI and Google Gemini Image.
