{
  pkgs,
  ...
}:

{
  packages = [ pkgs.git ];

  languages.python = {
    enable = true;
    uv = {
      enable = true;
      sync = {
        enable = true;
        allExtras = true;
        allGroups = true;
      };
    };

    venv = {
      enable = true;
    };

  };
}
