{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyMuprLYJpvgxWVeWPUuNnQm",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/pruizbarnada/BuzzerBeater/blob/main/Distribucion_minutos.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "0Qb0jaXyBcSZ"
      },
      "outputs": [],
      "source": [
        "import requests\n",
        "import xml.etree.ElementTree as ET\n",
        "import pandas as pd\n",
        "import openpyxl\n",
        "import pytz"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Funciones"
      ],
      "metadata": {
        "id": "kCbEcMWxBr1f"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def login(user, password, matchid):\n",
        "  base_url = \"http://bbapi.buzzerbeater.com/\"\n",
        "  params_autent = {\n",
        "        \"login\": user,\n",
        "        \"code\": password\n",
        "    }\n",
        "  session = requests.Session()\n",
        "  response = session.get(base_url, params=params_autent)\n",
        "  boxscore = session.get(base_url + 'boxscore.aspx', params = {'matchid':matchid})\n",
        "  xml_box = ET.fromstring(boxscore.content)\n",
        "\n",
        "  return xml_box"
      ],
      "metadata": {
        "id": "g2UMQWlrBjGj"
      },
      "execution_count": 39,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def find_minutes(xml_root, matchid):\n",
        "  with pd.ExcelWriter(f'minutes game {matchid}.xlsx', engine='openpyxl') as writer:\n",
        "\n",
        "    for team in ['awayTeam', 'homeTeam']:\n",
        "\n",
        "      df = pd.DataFrame(columns=[\"Jugador\", \"B\", \"E\", \"A\", \"AP\", \"P\", \"Titular\"])\n",
        "      team_code = xml_root.find(f\"./match/{team}/teamName\").text\n",
        "\n",
        "      for child in xml_root.findall(f\"./match/{team}/boxscore/player\"):\n",
        "        player = child.find(\"firstName\").text + \" \" + child.find(\"lastName\").text\n",
        "\n",
        "        pg = child.find(\"minutes/PG\").text\n",
        "        sg = child.find(\"minutes/SG\").text\n",
        "        sf = child.find(\"minutes/SF\").text\n",
        "        pf = child.find(\"minutes/PF\").text\n",
        "        c = child.find(\"minutes/C\").text\n",
        "\n",
        "        starter = child.find(\"isStarter\").text\n",
        "        if starter == \"True\":\n",
        "          starter = \"X\"\n",
        "        else:\n",
        "          starter = \"\"\n",
        "\n",
        "        new_row = [player, int(pg), int(sg), int(sf), int(pf), int(c), starter]\n",
        "        df.loc[len(df)] = new_row\n",
        "\n",
        "\n",
        "      df.to_excel(writer, sheet_name=team_code, index=False)\n",
        "\n",
        "\n",
        "  files.download(f'minutes game {matchid}.xlsx')"
      ],
      "metadata": {
        "id": "CACidZuCBnjj"
      },
      "execution_count": 40,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def minutes(user, password, matchid):\n",
        "  xml_boxscore = login(user, password, matchid)\n",
        "  find_minutes(xml_boxscore, matchid)\n",
        ""
      ],
      "metadata": {
        "id": "aDV764sDBnfi"
      },
      "execution_count": 41,
      "outputs": []
    },
    {
      "cell_type": "markdown",
      "source": [
        "#Generate excel"
      ],
      "metadata": {
        "id": "56PK2jqDO9Kj"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "user = \"olbap.\"\n",
        "password = \"25852\"\n",
        "matchid = 71764"
      ],
      "metadata": {
        "id": "J-jtYU1vO2yh"
      },
      "execution_count": 42,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "minutes(user, password, matchid)"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 17
        },
        "id": "dlfLU593O2wB",
        "outputId": "c3d51148-8ab5-41c3-bca8-c94fd0f472f4"
      },
      "execution_count": 44,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ],
            "application/javascript": [
              "\n",
              "    async function download(id, filename, size) {\n",
              "      if (!google.colab.kernel.accessAllowed) {\n",
              "        return;\n",
              "      }\n",
              "      const div = document.createElement('div');\n",
              "      const label = document.createElement('label');\n",
              "      label.textContent = `Downloading \"${filename}\": `;\n",
              "      div.appendChild(label);\n",
              "      const progress = document.createElement('progress');\n",
              "      progress.max = size;\n",
              "      div.appendChild(progress);\n",
              "      document.body.appendChild(div);\n",
              "\n",
              "      const buffers = [];\n",
              "      let downloaded = 0;\n",
              "\n",
              "      const channel = await google.colab.kernel.comms.open(id);\n",
              "      // Send a message to notify the kernel that we're ready.\n",
              "      channel.send({})\n",
              "\n",
              "      for await (const message of channel.messages) {\n",
              "        // Send a message to notify the kernel that we're ready.\n",
              "        channel.send({})\n",
              "        if (message.buffers) {\n",
              "          for (const buffer of message.buffers) {\n",
              "            buffers.push(buffer);\n",
              "            downloaded += buffer.byteLength;\n",
              "            progress.value = downloaded;\n",
              "          }\n",
              "        }\n",
              "      }\n",
              "      const blob = new Blob(buffers, {type: 'application/binary'});\n",
              "      const a = document.createElement('a');\n",
              "      a.href = window.URL.createObjectURL(blob);\n",
              "      a.download = filename;\n",
              "      div.appendChild(a);\n",
              "      a.click();\n",
              "      div.remove();\n",
              "    }\n",
              "  "
            ]
          },
          "metadata": {}
        },
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<IPython.core.display.Javascript object>"
            ],
            "application/javascript": [
              "download(\"download_3b08cabf-6512-4709-9488-cbb9f3ff76bd\", \"minutes game 71764.xlsx\", 6386)"
            ]
          },
          "metadata": {}
        }
      ]
    }
  ]
}