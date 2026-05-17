# -*- coding: utf-8 -*-
"""Planning-oriented prompt presets for GeoPrompt Urban Scenario Visualizer.

This module contains curated English prompt presets for urban and regional planning
scenario visualization. Presets are grouped into Basic, Intermediate, and Advanced
levels so users can move from simple clean-up and mapping tasks toward more complex
scenario simulation tasks.
"""

BASE_GUARDRAILS = (
    " Maintain geospatial coherence. Preserve the main road alignment, river geometry, coastline, parcel/block structure, "
    "and recognizable spatial layout as much as possible. Preserve the full frame and original apparent map scale. Do not crop, zoom, stretch, or reframe the image. Keep a top-down orthographic aerial/map view. "
    "Avoid fantasy elements, extreme perspective distortion, floating objects, text labels, logos, and unrealistic terrain changes. "
    "Treat the output as a planning scenario visualization, not an official legal map."
)

PROMPT_CATEGORIES = {
    "Basic / Clean & Prepare Base": [
        {
            "id": "clean_aerial_for_planning",
            "label": "Clean aerial base for planning",
            "prompt": "Clean and enhance this aerial or map image for urban planning presentation. Remove haze, visual noise, compression artifacts, and excessive shadows while keeping roads, buildings, vegetation, water, and land parcels recognizable." + BASE_GUARDRAILS,
        },
        {
            "id": "remove_visual_clutter",
            "label": "Remove visual clutter",
            "prompt": "Remove distracting visual clutter such as temporary objects, vehicles, construction debris, and random artifacts from the selected area. Reveal a clean planning base with clear ground surfaces, roads, open spaces, and building footprints." + BASE_GUARDRAILS,
        },
        {
            "id": "neutral_basemap",
            "label": "Neutral planning basemap",
            "prompt": "Transform this image into a neutral planning basemap. Simplify photographic textures into clean muted surfaces, keep roads and blocks legible, preserve buildings and green areas, and make the image suitable for overlaying GIS analysis layers." + BASE_GUARDRAILS,
        },
        {
            "id": "pre_development_clearance",
            "label": "Pre-development clearance",
            "prompt": "Visualize the selected underused or vacant parts as cleared pre-development land while keeping major roads, rivers, terrain edges, and surrounding buildings intact. The result should look realistic and useful for early site planning comparison." + BASE_GUARDRAILS,
        },
        {
            "id": "climate_ready_base",
            "label": "Climate-ready analysis base",
            "prompt": "Prepare a clear climate-ready planning base by enhancing visible drainage structure, open spaces, tree cover, and major circulation while simplifying visual clutter. Keep the image easy to read for resilience, adaptation, and vulnerability assessment discussions." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_first_base",
            "label": "Mobility-first base",
            "prompt": "Clean and enhance the selected area as a mobility-first planning base. Make roads, intersections, sidewalks, transit corridors, and open public spaces legible while preserving buildings and urban blocks for transport and accessibility planning." + BASE_GUARDRAILS,
        },
    ],
    "Basic / Add Planning Interventions": [
        {
            "id": "add_street_trees",
            "label": "Add shaded street trees",
            "prompt": "Add continuous rows of mature shade trees along both sides of visible primary and secondary streets. Keep the road network and existing buildings intact. Tree placement should improve pedestrian comfort without blocking intersections or access points." + BASE_GUARDRAILS,
        },
        {
            "id": "add_green_infrastructure",
            "label": "Add green infrastructure",
            "prompt": "Add urban green infrastructure including bioswales, rain gardens, permeable open spaces, pocket parks, vegetated medians, and riparian buffers where appropriate. Preserve the existing spatial structure and make the intervention look realistic for Strategic Environmental Assessment and climate adaptation planning." + BASE_GUARDRAILS,
        },
        {
            "id": "add_solar_rooftops",
            "label": "Add solar rooftops",
            "prompt": "Add realistic photovoltaic solar panels on suitable visible rooftops and selected open facility areas. Keep roof shapes, building footprints, roads, and surrounding land uses intact. The intervention should support a low-carbon urban development scenario." + BASE_GUARDRAILS,
        },
        {
            "id": "add_public_facilities",
            "label": "Add public facilities",
            "prompt": "Add small-scale public facilities in appropriate open or underserved areas, such as community centers, schools, health posts, plazas, shaded pedestrian spaces, and public service buildings. Match the local urban scale and avoid overbuilding." + BASE_GUARDRAILS,
        },
        {
            "id": "add_complete_streets",
            "label": "Add complete streets features",
            "prompt": "Retrofit the visible street network with complete streets features such as continuous sidewalks, safe crossings, bicycle lanes, bus stop improvements, curb extensions, shade trees, and traffic calming where appropriate. Preserve existing alignment and block structure." + BASE_GUARDRAILS,
        },
        {
            "id": "add_resilience_hubs",
            "label": "Add community resilience hubs",
            "prompt": "Add community resilience hubs in suitable public or institutional locations. Include small multi-purpose buildings, shaded gathering space, backup energy elements, water storage, emergency access, and inclusive public realm improvements while respecting the existing urban structure." + BASE_GUARDRAILS,
        },
    ],
    "Basic / Style & Planning Maps": [
        {
            "id": "detailed_spatial_plan_land_use_map",
            "label": "Detailed spatial plan land-use style",
            "prompt": "Transform this image into a clean detailed spatial plan land-use visualization. Use flat, distinct planning colors for residential, commercial, industrial, public facilities, green open space, agriculture, water, and roads only where those categories are visible. Keep boundaries clean and avoid photographic texture." + BASE_GUARDRAILS,
        },
        {
            "id": "figure_ground_urban_form",
            "label": "Figure-ground urban form",
            "prompt": "Generate a figure-ground urban form diagram. Represent all buildings and built structures as solid dark shapes with clean edges, and all non-built areas such as roads, open space, water, and vegetation as light background. No labels, no gradients, no decorative effects." + BASE_GUARDRAILS,
        },
        {
            "id": "conceptual_site_plan",
            "label": "Conceptual site plan",
            "prompt": "Transform the selected area into a clean conceptual site plan. Buildings should appear as simple footprints, roads as clear circulation lines, green areas as soft green blocks, water as blue surfaces, and public spaces as readable open areas. Presentation-ready planning graphic." + BASE_GUARDRAILS,
        },
        {
            "id": "planning_poster_map",
            "label": "Planning poster map",
            "prompt": "Create a polished urban planning poster map from this image. Use clean geometric forms, muted professional colors, high contrast between built areas, roads, water, and green spaces, and maintain realistic scale and spatial relationships. No fake labels or decorative text." + BASE_GUARDRAILS,
        },
        {
            "id": "urban_design_framework",
            "label": "Urban design framework map",
            "prompt": "Transform the selected area into an urban design framework graphic showing clear street structure, development blocks, open space hierarchy, blue-green systems, and key civic spaces in a clean professional planning style. Keep the layout map-like and presentation ready." + BASE_GUARDRAILS,
        },
        {
            "id": "blue_green_structure_plan",
            "label": "Blue-green structure plan",
            "prompt": "Create a blue-green structure plan graphic from the selected area. Emphasize waterways, drainage corridors, parks, green corridors, tree belts, retention landscapes, and ecological open spaces using a clean planning palette and diagrammatic style." + BASE_GUARDRAILS,
        },
    ],
    "Intermediate / Detection & Thematic Overlays": [
        {
            "id": "detect_building_overlay",
            "label": "Building footprint overlay",
            "prompt": "Detect visible buildings and built structures. Keep the original image visible and add a clean red outline around each building footprint. Use solid thin outlines, avoid filling non-building areas, and do not invent buildings that are not visible." + BASE_GUARDRAILS,
        },
        {
            "id": "detect_vegetation_overlay",
            "label": "Vegetation canopy overlay",
            "prompt": "Detect visible vegetation including tree canopy, parks, gardens, grass, and riparian vegetation. Keep the original image visible and outline vegetation zones in bright green with clean boundaries. Do not mark roads or buildings as vegetation." + BASE_GUARDRAILS,
        },
        {
            "id": "detect_impervious_surface",
            "label": "Impervious surface mask",
            "prompt": "Classify the visible area into impervious and pervious surfaces. Mark buildings, paved roads, parking lots, and hardscape in red. Mark vegetation, soil, water, and permeable open land in green. Use solid fills and clean boundaries, with no gradients." + BASE_GUARDRAILS,
        },
        {
            "id": "detect_blue_green_network",
            "label": "Blue-green network overlay",
            "prompt": "Identify and emphasize the blue-green network in the selected area. Highlight rivers, drainage channels, ponds, lakes, riparian corridors, parks, tree corridors, and connected green open spaces while keeping the original image visible underneath." + BASE_GUARDRAILS,
        },
        {
            "id": "detect_walkability_network",
            "label": "Walkability network overlay",
            "prompt": "Detect and emphasize the visible walkability network. Highlight sidewalks, crossing opportunities, small public spaces, school access corridors, transit access routes, and pedestrian-friendly street segments while keeping the underlying image visible." + BASE_GUARDRAILS,
        },
        {
            "id": "detect_heat_risk_priority",
            "label": "Heat-risk priority overlay",
            "prompt": "Create a heat-risk priority overlay by emphasizing highly exposed paved areas, low-canopy streets, sparse green zones, and large impervious surfaces as priority intervention areas, while distinguishing cooler green and blue spaces in the background." + BASE_GUARDRAILS,
        },
    ],
    "Intermediate / Mobility & Accessibility": [
        {
            "id": "mobility_bus_priority_corridor",
            "label": "Bus priority corridor",
            "prompt": "Transform the visible main corridor into a bus priority street with dedicated bus lanes, improved stops, clear pedestrian access, safer crossings, and organized curbside activity while preserving the existing street alignment and surrounding buildings." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_brt_retrofit",
            "label": "BRT street retrofit",
            "prompt": "Visualize a bus rapid transit retrofit with median or side-running BRT lanes, station platforms, pedestrian crossings, feeder access, and well-ordered public space. Keep the corridor realistic and suitable for transport planning presentation." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_safe_school_streets",
            "label": "Safe school streets",
            "prompt": "Rework the visible streets around schools or neighborhood facilities into a safe school streets scenario with lower traffic speed, wider sidewalks, crossing guards or refuge islands, tree shade, pickup-dropoff management, and child-friendly public space." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_cycling_network",
            "label": "Cycling network improvement",
            "prompt": "Add a coherent cycling network using protected bike lanes, neighborhood bikeways, secure crossings, and bicycle parking at key destinations while preserving the original street network and urban blocks." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_multimodal_interchange",
            "label": "Multimodal interchange area",
            "prompt": "Visualize a multimodal interchange area with smooth transfers between buses, walking, cycling, ride-hailing, and local access. Add organized circulation, waiting space, shade, and legible access paths while keeping the transport node realistic and top-down." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_pedestrianized_center",
            "label": "Pedestrianized town center",
            "prompt": "Transform the selected commercial or civic center into a pedestrian-priority area with widened sidewalks, limited vehicle access, shaded seating, public space programming, and active street edges. Preserve the existing urban pattern while clearly improving walkability." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_last_mile_access",
            "label": "Last-mile transit access",
            "prompt": "Improve last-mile access to transit by adding clear walking routes, bicycle access, feeder stops, pickup zones, and safe crossings between neighborhoods and transit stations or stops. Keep the broader spatial layout intact." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_station_area_accessibility",
            "label": "Station area accessibility",
            "prompt": "Visualize station area accessibility improvements such as barrier-free pedestrian routes, bicycle parking, shade, plazas, direct crossing paths, and better frontage organization around a rail or transit station." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_curb_management",
            "label": "Curb management and street logistics",
            "prompt": "Organize the visible streetscape with designated loading zones, curbside management, passenger pick-up areas, micro-logistics space, and pedestrian protection measures while reducing random parking and keeping traffic circulation legible." + BASE_GUARDRAILS,
        },
        {
            "id": "mobility_traffic_calming_neighborhood",
            "label": "Traffic-calmed neighborhood",
            "prompt": "Transform the neighborhood street network into a traffic-calmed scenario with reduced roadway dominance, raised crossings, curb extensions, safer intersections, tree planting, and more people-oriented public space." + BASE_GUARDRAILS,
        },
    ],
    "Intermediate / Land Use, Zoning & Development Control": [
        {
            "id": "zoning_residential_structure",
            "label": "Residential zoning structure",
            "prompt": "Render the selected area as a clean residential zoning structure plan. Clearly distinguish lower-density and medium-density residential areas, local streets, public facilities, open space, and compatible neighborhood commercial edges using a professional planning-map style." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_mixed_use_intensity",
            "label": "Mixed-use intensity zoning",
            "prompt": "Transform the area into a mixed-use intensity zoning concept showing higher-intensity mixed-use zones on main corridors, moderate neighborhood mixed-use zones near centers, and compatible residential areas behind them. Use clean block-based planning colors and maintain readable parcel or block structure." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_industrial_buffer_control",
            "label": "Industrial buffer control",
            "prompt": "Visualize industrial zoning with clear buffer treatment between industrial land, housing, public facilities, roads, and green edges. Show a controlled spatial relationship that improves land-use compatibility and environmental protection." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_green_open_space_protection",
            "label": "Green open space protection",
            "prompt": "Create a land-use control graphic that emphasizes protected green open space, parks, river buffers, ecological corridors, and restricted development zones. Keep the built-up areas legible but secondary to the protected open-space network." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_waterfront_setback_control",
            "label": "Waterfront setback control",
            "prompt": "Visualize development control along the waterfront or river corridor using clear setback zones, riparian protection areas, public access strips, and controlled development areas beyond the buffer." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_urban_growth_boundary",
            "label": "Urban growth boundary concept",
            "prompt": "Render the area as an urban growth boundary concept that differentiates priority urban development areas, controlled expansion areas, rural or agricultural protection zones, and major infrastructure corridors in a clear planning-map style." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_transit_supportive_intensity",
            "label": "Transit-supportive intensity zoning",
            "prompt": "Visualize transit-supportive zoning with higher development intensity near transit corridors or stations, moderate transition zones, and lower-intensity surrounding neighborhoods. Keep the result clean, block-based, and suitable for presentation in a detailed spatial plan context." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_heritage_conservation_control",
            "label": "Heritage conservation control",
            "prompt": "Create a conservation-oriented zoning graphic that identifies heritage preservation zones, adaptive reuse areas, contextual infill controls, public realm protection, and tourism-supportive areas while preserving the recognizable street and block pattern." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_infill_redevelopment_control",
            "label": "Infill redevelopment control",
            "prompt": "Visualize infill redevelopment control by distinguishing redevelopment opportunity sites, preserved urban fabric, public facility land, open space, and corridor intensification areas. Use a professional planning-map style with clean edges and clear block structure." + BASE_GUARDRAILS,
        },
        {
            "id": "zoning_public_facility_reservation",
            "label": "Public facility reservation map",
            "prompt": "Transform the area into a public facility reservation and development control map showing land reserved for schools, health facilities, civic buildings, utilities, open space, transport support, and future community services. Keep the map clean and realistic." + BASE_GUARDRAILS,
        },
    ],
    "Advanced / Urban Scenario Simulation": [
        {
            "id": "simulate_tod_corridor",
            "label": "Transit-oriented development corridor",
            "prompt": "Convert the selected corridor into a transit-oriented development scenario. Add compact mixed-use buildings near transit nodes, shaded sidewalks, bicycle lanes, bus stops, pedestrian plazas, active frontages, and organized public space. Keep the main road alignment recognizable." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_compact_mixed_use",
            "label": "Compact mixed-use district",
            "prompt": "Transform underused or low-intensity parts of the selected area into a compact mixed-use urban district with medium-density buildings, walkable blocks, ground-floor activity, public open spaces, and integrated greenery. Blend with surrounding urban form." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_flood_resilience",
            "label": "Flood resilience scenario",
            "prompt": "Visualize a flood-resilient urban scenario. Add retention ponds, restored drainage corridors, permeable surfaces, elevated critical access, riparian buffers, and blue-green infrastructure. Keep existing buildings and major road structure recognizable unless adaptation requires small realistic modifications." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_low_carbon_city",
            "label": "Low-carbon city scenario",
            "prompt": "Transform the selected area into a low-carbon urban development scenario with solar rooftops, tree canopy, cool roofs, compact land use, pedestrian-friendly streets, bicycle infrastructure, and more permeable surfaces. Keep the spatial layout realistic and top-down." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_tourism_corridor",
            "label": "Tourism corridor scenario",
            "prompt": "Visualize the selected street or district as an attractive tourism corridor with shaded pedestrian paths, active storefronts, wayfinding plazas, small public spaces, landscape improvements, cultural streetscape elements, and organized parking or access. Avoid theme-park fantasy." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_post_mining_city",
            "label": "Post-mining city recovery",
            "prompt": "Transform degraded, quarry, or post-mining land into a resilient post-mining city recovery scenario. Add ecological restoration, water retention landscapes, safe public access, productive green areas, community facilities, and compact development only where appropriate." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_urban_heat_mitigation",
            "label": "Urban heat mitigation",
            "prompt": "Visualize urban heat mitigation interventions. Add dense shade trees, cool roofs, reflective pavements where suitable, pocket parks, shaded pedestrian corridors, and blue-green cooling elements. Preserve buildings and main circulation but improve thermal comfort visibly." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_riverfront_regeneration",
            "label": "Riverfront regeneration",
            "prompt": "Regenerate the visible riverfront or water edge into a safe, green, accessible public corridor. Add riparian buffers, walking paths, floodable parks, small plazas, ecological planting, and controlled building orientation toward the waterfront while preserving the river geometry." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_fifteen_minute_neighborhood",
            "label": "15-minute neighborhood",
            "prompt": "Transform the selected district into a 15-minute neighborhood scenario with walkable local streets, mixed daily services, schools, health access, small public spaces, bicycle connections, shade, and compact neighborhood-scale amenities distributed within easy reach of residents." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_sponge_city",
            "label": "Sponge city scenario",
            "prompt": "Visualize a sponge city scenario using nature-based stormwater solutions such as bioswales, retention landscapes, rain gardens, restored channels, permeable surfaces, and floodable open space while preserving the recognizable urban structure." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_net_zero_district",
            "label": "Net-zero district",
            "prompt": "Transform the selected area into a net-zero district scenario with solar rooftops, efficient compact blocks, shaded low-emission streets, blue-green infrastructure, reduced parking dominance, and pedestrian-priority public spaces, while keeping the layout realistic and map-like." + BASE_GUARDRAILS,
        },
        {
            "id": "simulate_inclusive_public_realm",
            "label": "Inclusive public realm",
            "prompt": "Visualize an inclusive public realm scenario with barrier-free sidewalks, universal access crossings, shaded seating, safe public gathering spaces, child-friendly and elderly-friendly design features, and equitable access to services across the selected area." + BASE_GUARDRAILS,
        },
    ],
}


def all_presets_flat():
    rows = []
    for cat, presets in PROMPT_CATEGORIES.items():
        for p in presets:
            rows.append({"category": cat, **p})
    return rows
