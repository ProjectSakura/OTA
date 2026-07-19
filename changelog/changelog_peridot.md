# Changelog

## Jul 16, 2026
- XiaomiParts Rework: separate notification/icon for GamingProfile
- XiaomiParts Rework: PowerProfile control settings screen
- XiaomiParts Rework: Charge Control settings screen
- XiaomiParts Rework: launcher in app drawer
- Fix Touch Sampling QS tile long-press routing
- Update product partition reserved space
- Revert config power decouple mode
- Optimize native executables for Cortex-A76
- Fix EINVAL spam from write-only bump_sample_rate node
- Debloat: drop Aperture

## Jul 15, 2026
- Reduce system server verbosity
- Use foreground cpuset/uclamp for gralloc
- Use foreground uclamp for hwcomposer
- Enable R8 optimizations for system_server and SystemUI
- Compile HWUI for performance
- Enable full ART optimizations with VDEX/ODEX
- Enable ADPF CPU hints for improved UI performance
- Wifi: enable optimized power management
- Wifi: enable QPower and deep sleep simultaneously
- RIL edits for battery life
- Improve auto brightness
- Optimize auto brightness adjustment
- Enable Qualcomm TrueWireless Stereo
- Enable support for kernel idle timer
- Smoother scrolling and better responsiveness

## Jul 01, 2026
Device changelogs:
- Initial ChangeLog
- Clean Rebased DeviceTree
- Refined interaction and scheduler parameters.
- Disabled Skia tracing by default.
- Implemented ChargeControl Qs Service and performed associated refactoring.
- Added a gaming mode profile to PowerProfileTileServices
- Included MiuiCamera.
- Dropped Aperture
- Resolved SELinux policy denials, specifically for Diag-router and bring-up.
- Disabled htsr on profile toggle.
- Disabled ART debug settings.
- Disabled some Wlan debugs.
- Dynamic Dalvik Heap Implimented
- And Many More...

Kernel changelogs:
- Initial ChangeLog
- Enabled BBR And More TCP congestion control
- Added DroidSpace Support
